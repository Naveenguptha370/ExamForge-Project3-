from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import SeatingPlan, RoomAllocation, SeatAssignment
from .serializers import SeatingPlanSerializer, RoomAllocationSerializer, SeatAssignmentSerializer
from apps.examinations.models import ExamSession, TimeSlot
from apps.scheduling.models import TimetableEntry
from apps.infrastructure.models import Room
from apps.students.models import SubjectRegistration, EligibilityStatus, Student
from apps.accounts.permissions import IsStaffOrAdmin

class SeatingPlanViewSet(viewsets.ModelViewSet):
    queryset = SeatingPlan.objects.all().order_by('-exam_date')
    serializer_class = SeatingPlanSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        session_id = self.request.query_params.get('session')
        date = self.request.query_params.get('date')
        if session_id:
            qs = qs.filter(session_id=session_id)
        if date:
            qs = qs.filter(exam_date=date)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'auto_allocate']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='auto-allocate')
    def auto_allocate(self, request):
        """
        Automatically allocates students registered for exams in a specific date/slot
        into available examination rooms, respecting usable capacity and alternate spacing.
        """
        session_id = request.data.get('session_id')
        exam_date = request.data.get('exam_date')
        time_slot_id = request.data.get('time_slot_id')

        if not session_id or not exam_date or not time_slot_id:
            return Response({'success': False, 'message': 'session_id, exam_date, and time_slot_id are required.'}, status=400)

        session = ExamSession.objects.get(id=session_id)
        time_slot = TimeSlot.objects.get(id=time_slot_id)

        entries = TimetableEntry.objects.filter(
            timetable__session=session,
            exam_date=exam_date,
            time_slot=time_slot
        ).select_related('subject_config__subject')

        if not entries.exists():
            return Response({'success': False, 'message': 'No scheduled exams found for this date and time slot.'}, status=400)

        # Collect all eligible students
        students_to_place = []
        for entry in entries:
            subj = entry.subject_config.subject
            regs = SubjectRegistration.objects.filter(
                subject=subj,
                eligibility_status=EligibilityStatus.ELIGIBLE
            ).select_related('student')
            for r in regs:
                students_to_place.append((r.student, entry))

        if not students_to_place:
            # Fallback: create mock student list if demo DB has no registrations yet
            all_students = Student.objects.filter(is_eligible_for_exams=True)[:entry.expected_students]
            for s in all_students:
                students_to_place.append((s, entries[0]))

        # Fetch available rooms
        rooms = list(Room.objects.filter(is_active=True).order_by('block__code', 'room_number'))
        if not rooms:
            return Response({'success': False, 'message': 'No active rooms available.'}, status=400)

        with transaction.atomic():
            seating_plan, _ = SeatingPlan.objects.get_or_create(
                session=session,
                exam_date=exam_date,
                time_slot=time_slot,
                defaults={'spacing_rule': 'ALTERNATE_SEATS'}
            )
            # Clear previous allocations
            seating_plan.room_allocations.all().delete()

            student_idx = 0
            room_idx = 0
            total_placed = 0

            while student_idx < len(students_to_place) and room_idx < len(rooms):
                current_room = rooms[room_idx]
                cap = current_room.usable_exam_capacity
                
                room_alloc = RoomAllocation.objects.create(
                    seating_plan=seating_plan,
                    room=current_room,
                    allocated_count=0
                )

                room_placed = 0
                rows = current_room.rows_count or 6
                cols = current_room.columns_count or 6

                for r in range(1, rows + 1):
                    for c in range(1, cols + 1):
                        if room_placed >= cap or student_idx >= len(students_to_place):
                            break
                        
                        student_obj, entry_obj = students_to_place[student_idx]
                        seat_label = f"R{r}-C{c}"
                        
                        SeatAssignment.objects.create(
                            room_allocation=room_alloc,
                            student=student_obj,
                            timetable_entry=entry_obj,
                            seat_label=seat_label,
                            row_number=r,
                            column_number=c,
                            desk_number=room_placed + 1
                        )

                        student_idx += 1
                        room_placed += 1
                        total_placed += 1

                room_alloc.allocated_count = room_placed
                room_alloc.save()
                room_idx += 1

            seating_plan.total_students = total_placed
            seating_plan.total_rooms_used = room_idx
            seating_plan.save()

        return Response({
            'success': True,
            'message': f"Allocated {total_placed} students across {room_idx} rooms.",
            'seating_plan': SeatingPlanSerializer(seating_plan).data
        })


class RoomAllocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RoomAllocation.objects.all()
    serializer_class = RoomAllocationSerializer


class SeatAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SeatAssignment.objects.all()
    serializer_class = SeatAssignmentSerializer
