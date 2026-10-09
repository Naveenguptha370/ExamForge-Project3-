from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from examinations.models import Examination
from infrastructure.models import Room, RoomAssignment
from academics.models import Faculty, FacultyLeave
from .models import InvigilatorDuty, DutyRequirement


class InvigilatorAllocationEngine:
    """
    Engine for automatic invigilator assignment, availability checking,
    fair workload distribution, and overlapping duty prevention.
    """

    @classmethod
    def allocate(cls, examination_id: int, ratio_per_students: int = 30, balance_workload: bool = True):
        exam = Examination.objects.select_related('subject', 'session', 'time_slot').get(id=examination_id)
        
        # 1. Fetch assigned rooms for this exam
        room_assignments = list(RoomAssignment.objects.filter(examination=exam).select_related('room', 'room__building'))
        if not room_assignments:
            raise ValidationError("No rooms have been assigned to this examination yet. Please generate seating first.")

        duty_date = exam.exam_date
        time_slot = exam.time_slot

        # 2. Determine required invigilators per room
        room_needs = []
        for ra in room_assignments:
            # e.g., 1 invigilator for <= 30 students, 2 for > 30 students
            student_count = ra.allotted_students_count
            if student_count <= 0:
                needed = 1
            else:
                needed = max(1, (student_count + ratio_per_students - 1) // ratio_per_students)
            
            # Save or update DutyRequirement
            req, _ = DutyRequirement.objects.get_or_create(
                examination=exam,
                room=ra.room,
                defaults={'required_invigilators': needed}
            )
            req.required_invigilators = needed
            req.save()

            room_needs.append({
                'room': ra.room,
                'student_count': student_count,
                'needed': needed
            })

        total_invigilators_needed = sum(rn['needed'] for rn in room_needs)

        # 3. Identify all eligible faculty members
        all_faculty = Faculty.objects.filter(is_active=True).select_related('department')

        # 3a. Filter out faculty on approved leave
        leaves = FacultyLeave.objects.filter(
            is_approved=True,
            start_date__lte=duty_date,
            end_date__gte=duty_date
        )
        faculty_on_leave_ids = set(leaves.values_list('faculty_id', flat=True))

        # 3b. Filter out faculty already assigned to ANOTHER room or exam at this date & time slot
        # Exclude duties from THIS examination being regenerated
        conflicting_duties = InvigilatorDuty.objects.filter(
            duty_date=duty_date,
            time_slot=time_slot
        ).exclude(examination=exam)
        faculty_with_conflicts_ids = set(conflicting_duties.values_list('faculty_id', flat=True))

        unavailable_ids = faculty_on_leave_ids.union(faculty_with_conflicts_ids)
        available_faculty = [f for f in all_faculty if f.id not in unavailable_ids]

        # 4. Workload balancing: calculate existing duties across current session
        duty_counts = {
            f.id: InvigilatorDuty.objects.filter(
                faculty=f,
                examination__session=exam.session
            ).exclude(examination=exam).count()
            for f in available_faculty
        }

        # Sort available faculty by (duties_count, designation hierarchy)
        if balance_workload:
            available_faculty.sort(key=lambda f: (duty_counts.get(f.id, 0), f.id))

        # 5. Perform Assignment
        with transaction.atomic():
            # Clear existing duties for this examination
            InvigilatorDuty.objects.filter(examination=exam).delete()

            duties_created = []
            faculty_idx = 0
            unstaffed_rooms = []

            for rn in room_needs:
                room = rn['room']
                needed = rn['needed']
                assigned_to_this_room = 0

                for i in range(needed):
                    if faculty_idx < len(available_faculty):
                        fac = available_faculty[faculty_idx]
                        faculty_idx += 1
                        assigned_to_this_room += 1

                        role = 'chief_superintendent' if i == 0 and rn['student_count'] > 30 else 'hall_invigilator'
                        duty = InvigilatorDuty(
                            examination=exam,
                            room=room,
                            faculty=fac,
                            duty_date=duty_date,
                            time_slot=time_slot,
                            role=role,
                            status='assigned',
                            notes=f"Auto-assigned with workload index {duty_counts.get(fac.id, 0)}"
                        )
                        duties_created.append(duty)
                    else:
                        break

                if assigned_to_this_room < needed:
                    shortage = needed - assigned_to_this_room
                    unstaffed_rooms.append({
                        'room_number': room.room_number,
                        'building': room.building.name,
                        'shortage': shortage,
                        'message': f"Shortage of {shortage} invigilator(s) in Room {room.room_number}"
                    })

            InvigilatorDuty.objects.bulk_create(duties_created)

            # Update exam status
            if exam.status in ['scheduled', 'seating_generated']:
                exam.status = 'invigilators_assigned'
                exam.save()

        return {
            'examination_id': exam.id,
            'subject_code': exam.subject.code,
            'exam_date': exam.exam_date,
            'time_slot': exam.time_slot.name,
            'total_needed': total_invigilators_needed,
            'total_assigned': len(duties_created),
            'available_faculty_count': len(available_faculty),
            'faculty_on_leave_count': len(faculty_on_leave_ids),
            'faculty_slot_conflict_count': len(faculty_with_conflicts_ids),
            'unstaffed_rooms': unstaffed_rooms,
            'is_fully_staffed': len(unstaffed_rooms) == 0
        }

    @classmethod
    def reassign_duty(cls, duty_id: int, new_faculty_id: int):
        """
        Manually reassigns a duty to another faculty member with immediate conflict checks.
        """
        duty = InvigilatorDuty.objects.select_related('examination', 'room', 'time_slot').get(id=duty_id)
        new_faculty = Faculty.objects.get(id=new_faculty_id)

        if not new_faculty.is_active:
            raise ValidationError(f"Faculty {new_faculty.name} is currently inactive.")

        # Check leave
        leave = FacultyLeave.objects.filter(
            faculty=new_faculty,
            is_approved=True,
            start_date__lte=duty.duty_date,
            end_date__gte=duty.duty_date
        ).first()
        if leave:
            raise ValidationError(f"Faculty {new_faculty.name} is on approved leave from {leave.start_date} to {leave.end_date} ({leave.reason}).")

        # Check overlapping duty
        conflict = InvigilatorDuty.objects.filter(
            duty_date=duty.duty_date,
            time_slot=duty.time_slot,
            faculty=new_faculty
        ).exclude(id=duty.id).select_related('room', 'examination__subject').first()

        if conflict:
            raise ValidationError(
                f"Faculty {new_faculty.name} is already assigned to {conflict.examination.subject.code} "
                f"in Room {conflict.room.room_number} during this time slot."
            )

        old_faculty_name = duty.faculty.name
        duty.faculty = new_faculty
        duty.status = 'reassigned'
        duty.notes = f"Manually reassigned from {old_faculty_name} to {new_faculty.name}"
        duty.save()

        return {
            'success': True,
            'message': f"Duty in Room {duty.room.room_number} reassigned to {new_faculty.name}",
            'new_faculty_name': new_faculty.name
        }

    @classmethod
    def get_faculty_workload_stats(cls):
        """
        Calculates workload distribution across all faculty members.
        """
        faculty_list = Faculty.objects.filter(is_active=True).select_related('department')
        workloads = []

        for f in faculty_list:
            total_duties = InvigilatorDuty.objects.filter(faculty=f).count()
            duties_this_month = InvigilatorDuty.objects.filter(faculty=f).count() # or filter by date
            utilization = round((total_duties / f.max_weekly_duties * 100), 1) if f.max_weekly_duties > 0 else 0

            workloads.append({
                'id': f.id,
                'name': f.name,
                'employee_id': f.employee_id,
                'department': f.department.code,
                'designation': f.designation,
                'total_duties': total_duties,
                'max_duties': f.max_weekly_duties,
                'utilization_percent': min(utilization, 100),
                'email': f.email,
                'phone': f.phone
            })

        workloads.sort(key=lambda x: -x['total_duties'])
        return workloads
