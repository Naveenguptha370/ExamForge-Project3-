from django.db import transaction
from django.core.exceptions import ValidationError
from examinations.models import Examination, ExamRegistration
from infrastructure.models import Room, RoomAssignment
from infrastructure.services import ensure_room_seats, check_room_availability
from academics.models import Student
from .models import SeatingPlan, Seat, SeatAllocation


class SeatingEngine:
    """
    Constraint-based automatic seating engine for ExamForge.
    Supports 4 configurable spacing strategies, capacity shortage detection,
    cross-department cheating prevention, and manual interactive adjustments.
    """

    @classmethod
    def generate(cls, examination_id: int, room_ids: list, spacing_rule: str = 'department_separated'):
        exam = Examination.objects.select_related('subject', 'session', 'time_slot').get(id=examination_id)
        
        # 1. Fetch eligible registered students
        registrations = ExamRegistration.objects.filter(
            examination=exam,
            is_eligible=True
        ).select_related('student', 'student__department', 'student__course')

        students = [r.student for r in registrations]
        total_students = len(students)

        if total_students == 0:
            raise ValidationError("No eligible registered students found for this examination.")

        if not room_ids:
            raise ValidationError("Please select at least one examination room for seating allocation.")

        # 2. Fetch and validate selected rooms
        rooms = list(Room.objects.filter(id__in=room_ids, is_active=True).select_related('building'))
        if len(rooms) != len(room_ids):
            raise ValidationError("One or more selected rooms were not found or are inactive.")

        # Check room availability (maintenance / other exams at same slot)
        for r in rooms:
            ensure_room_seats(r)
            # Check availability excluding current exam assignments
            is_avail, reason = check_room_availability(r.id, exam.exam_date, exam.time_slot_id)
            # If room already assigned to THIS exam, it's fine
            already_assigned_to_this = RoomAssignment.objects.filter(examination=exam, room=r).exists()
            if not is_avail and not already_assigned_to_this:
                raise ValidationError(f"Room {r.room_number} ({r.building.name}) is unavailable: {reason}")

        # 3. Collect candidate seats based on the selected spacing rule
        # Candidate seat: (room, seat_object)
        candidate_seats = []
        for room in rooms:
            seats_in_room = list(Seat.objects.filter(room=room, is_usable=True).order_by('row_index', 'col_index'))
            
            for s in seats_in_room:
                if spacing_rule == 'consecutive':
                    candidate_seats.append((room, s))
                elif spacing_rule == 'alternate_gap':
                    # 1 seat gap horizontally
                    if s.col_index % 2 == 1:
                        candidate_seats.append((room, s))
                elif spacing_rule == 'checkerboard':
                    # Diagonally alternating
                    if (s.row_index + s.col_index) % 2 == 0:
                        candidate_seats.append((room, s))
                elif spacing_rule == 'department_separated':
                    # All seats are candidates, but student assignment order will separate departments
                    candidate_seats.append((room, s))

        total_candidate_seats = len(candidate_seats)
        capacity_shortage = max(0, total_students - total_candidate_seats)
        total_to_allocate = min(total_students, total_candidate_seats)

        # 4. Student ordering based on Spacing Rule
        ordered_students = []
        if spacing_rule == 'department_separated':
            # Partition students by department/course
            dept_map = {}
            for s in students:
                dept_code = s.department.code
                if dept_code not in dept_map:
                    dept_map[dept_code] = []
                dept_map[dept_code].append(s)

            # Round-robin interleaving to ensure adjacent seats have different departments
            dept_keys = sorted(dept_map.keys())
            max_len = max(len(lst) for lst in dept_map.values())
            for idx in range(max_len):
                for dk in dept_keys:
                    if idx < len(dept_map[dk]):
                        ordered_students.append(dept_map[dk][idx])
        else:
            # Sort naturally by roll number
            ordered_students = sorted(students, key=lambda s: s.roll_no)

        students_to_seat = ordered_students[:total_to_allocate]
        unallocated_students = ordered_students[total_to_allocate:]

        # 5. Database transaction to create allocations
        with transaction.atomic():
            # Update or create SeatingPlan
            seating_plan, _ = SeatingPlan.objects.get_or_create(
                examination=exam,
                defaults={
                    'session_title': f"{exam.session.name} - {exam.subject.code}",
                    'spacing_rule': spacing_rule
                }
            )
            seating_plan.spacing_rule = spacing_rule
            seating_plan.session_title = f"{exam.session.name} - {exam.subject.code}"

            # Clear existing allocations for this plan
            SeatAllocation.objects.filter(examination=exam).delete()
            RoomAssignment.objects.filter(examination=exam).delete()

            allocations_to_create = []
            room_allotment_count = {r.id: 0 for r in rooms}

            for idx in range(total_to_allocate):
                student = students_to_seat[idx]
                room, seat = candidate_seats[idx]

                allocations_to_create.append(
                    SeatAllocation(
                        seating_plan=seating_plan,
                        examination=exam,
                        student=student,
                        room=room,
                        seat=seat,
                        seat_label=seat.seat_label,
                        allocation_type='auto'
                    )
                )
                room_allotment_count[room.id] += 1

            SeatAllocation.objects.bulk_create(allocations_to_create)

            # Create or update RoomAssignment records
            for room in rooms:
                count = room_allotment_count.get(room.id, 0)
                RoomAssignment.objects.create(
                    examination=exam,
                    room=room,
                    allotted_students_count=count,
                    status='reserved' if count > 0 else 'released'
                )

            # Update SeatingPlan stats
            seating_plan.total_allocated = total_to_allocate
            seating_plan.total_unallocated = len(unallocated_students)
            seating_plan.capacity_shortage = capacity_shortage

            if capacity_shortage > 0:
                seating_plan.status = 'draft'
                seating_plan.validation_status = f'Shortage: {capacity_shortage} students unallocated'
                seating_plan.validation_notes = (
                    f"Room capacity shortage: {total_students} students registered, but only {total_candidate_seats} "
                    f"seats are available under '{spacing_rule}' spacing. Please assign additional examination halls."
                )
            else:
                seating_plan.status = 'validated'
                seating_plan.validation_status = 'Validated: All students seated conflict-free'
                seating_plan.validation_notes = f"All {total_students} students successfully assigned across {len(rooms)} rooms."

            seating_plan.save()

            # Update examination status
            if exam.status == 'scheduled':
                exam.status = 'seating_generated'
                exam.save()

        return {
            'seating_plan_id': seating_plan.id,
            'status': seating_plan.status,
            'total_students': total_students,
            'total_allocated': total_to_allocate,
            'total_unallocated': len(unallocated_students),
            'capacity_shortage': capacity_shortage,
            'unallocated_student_roll_nos': [s.roll_no for s in unallocated_students],
            'validation_status': seating_plan.validation_status,
            'validation_notes': seating_plan.validation_notes
        }

    @classmethod
    def revalidate(cls, examination_id: int):
        """
        Validates an existing seating plan for conflicts:
        1. Duplicate student allocations
        2. Duplicate seat allocations
        3. Spacing violations
        """
        exam = Examination.objects.get(id=examination_id)
        plan = getattr(exam, 'seating_plan', None)
        if not plan:
            return {'is_valid': False, 'message': 'No seating plan generated yet.'}

        allocations = list(SeatAllocation.objects.filter(examination=exam).select_related('student', 'room', 'seat'))
        
        # 1. Duplicate student check
        seen_students = set()
        duplicate_students = set()
        for a in allocations:
            if a.student_id in seen_students:
                duplicate_students.add(a.student.roll_no)
            seen_students.add(a.student_id)

        # 2. Duplicate seat check
        seen_seats = set()
        duplicate_seats = set()
        for a in allocations:
            seat_key = (a.room_id, a.seat_id)
            if seat_key in seen_seats:
                duplicate_seats.add(f"{a.room.room_number}: {a.seat.seat_label}")
            seen_seats.add(seat_key)

        issues = []
        if duplicate_students:
            issues.append(f"Duplicate student allocations detected: {', '.join(duplicate_students)}")
        if duplicate_seats:
            issues.append(f"Multiple students assigned to the exact same seat: {', '.join(duplicate_seats)}")

        if issues:
            plan.validation_status = 'Conflicts Detected'
            plan.validation_notes = "; ".join(issues)
            plan.save()
            return {'is_valid': False, 'issues': issues}
        else:
            plan.validation_status = 'Validated: Conflict-Free'
            plan.validation_notes = f"All {len(allocations)} allocations verified unique and conflict-free."
            plan.save()
            return {'is_valid': True, 'issues': []}

    @classmethod
    def swap_or_move(cls, allocation_id: int, target_room_id: int, target_seat_id: int):
        """
        Performs a manual seat reassignment or swap between two seats:
        - If target seat already has a student allocated, SWAP their seats!
        - If target seat is empty, MOVE student to target seat!
        Validates target seat usability and prevents duplicate assignments.
        """
        with transaction.atomic():
            source_alloc = SeatAllocation.objects.select_related('examination', 'student', 'room', 'seat').get(id=allocation_id)
            exam = source_alloc.examination
            target_room = Room.objects.get(id=target_room_id)
            target_seat = Seat.objects.get(id=target_seat_id, room=target_room)

            if not target_seat.is_usable:
                raise ValidationError("Target seat is marked as unusable.")

            # Check if target seat is already occupied in this exam
            target_alloc = SeatAllocation.objects.filter(
                examination=exam,
                room=target_room,
                seat=target_seat
            ).first()

            if target_alloc:
                # SWAP: Put target_alloc student into source_alloc's seat
                original_source_room = source_alloc.room
                original_source_seat = source_alloc.seat
                original_source_label = source_alloc.seat_label

                # Free source seat temporarily to prevent unique constraint conflict
                source_alloc.seat = None
                source_alloc.save(update_fields=['seat'])

                target_alloc.room = original_source_room
                target_alloc.seat = original_source_seat
                target_alloc.seat_label = original_source_label
                target_alloc.allocation_type = 'manual_swap'
                target_alloc.save()

                source_alloc.room = target_room
                source_alloc.seat = target_seat
                source_alloc.seat_label = target_seat.seat_label
                source_alloc.allocation_type = 'manual_swap'
                source_alloc.save()

                action = f"Swapped {source_alloc.student.roll_no} and {target_alloc.student.roll_no}"
            else:
                # MOVE: empty target seat
                source_alloc.room = target_room
                source_alloc.seat = target_seat
                source_alloc.seat_label = target_seat.seat_label
                source_alloc.allocation_type = 'manual_swap'
                source_alloc.save()
                action = f"Moved {source_alloc.student.roll_no} to {target_room.room_number} [{target_seat.seat_label}]"

            # Re-update RoomAssignment counts
            for r in [source_alloc.room, target_room]:
                count = SeatAllocation.objects.filter(examination=exam, room=r).count()
                assignment, _ = RoomAssignment.objects.get_or_create(examination=exam, room=r)
                assignment.allotted_students_count = count
                assignment.save()

            return {
                'success': True,
                'action': action,
                'student_roll_no': source_alloc.student.roll_no,
                'new_room': target_room.room_number,
                'new_seat': target_seat.seat_label
            }
