from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Seat, SeatingPlan, SeatAllocation
from .serializers import SeatingPlanSerializer, SeatAllocationSerializer, SeatSerializer
from apps.infrastructure.models import ExaminationRoom
from apps.examinations.models import ExamSubject
from apps.registration.models import SubjectRegistration
from apps.students.models import StudentProfile

class SeatingPlanViewSet(viewsets.ModelViewSet):
    queryset = SeatingPlan.objects.select_related('exam_subject__subject', 'room__building').prefetch_related('allocations__seat', 'allocations__student').all()
    serializer_class = SeatingPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        exam_subject_id = self.request.query_params.get('exam_subject')
        room_id = self.request.query_params.get('room')
        if exam_subject_id:
            qs = qs.filter(exam_subject_id=exam_subject_id)
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs

    @action(detail=False, methods=['post'])
    def generate_plan(self, request):
        exam_subject_id = request.data.get('exam_subject_id')
        room_ids = request.data.get('room_ids', [])
        spacing_rule = request.data.get('spacing_rule', 'ALTERNATE_COLS')

        if not exam_subject_id:
            return Response({'error': 'exam_subject_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        exam_subject = ExamSubject.objects.filter(id=exam_subject_id).select_related('subject').first()
        if not exam_subject:
            return Response({'error': 'Exam subject not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get all eligible students registered for this subject
        registered_student_ids = list(SubjectRegistration.objects.filter(
            subject=exam_subject.subject,
            is_approved=True,
            eligibility_status='ELIGIBLE'
        ).values_list('student_id', flat=True))

        students = list(StudentProfile.objects.filter(id__in=registered_student_ids).order_by('roll_no'))
        total_students = len(students)

        if not room_ids:
            # Auto select available rooms with sufficient capacity
            room_ids = list(ExaminationRoom.objects.filter(status='AVAILABLE').order_by('-usable_capacity').values_list('id', flat=True))

        rooms = list(ExaminationRoom.objects.filter(id__in=room_ids, status='AVAILABLE'))
        if not rooms:
            return Response({'error': 'No available examination rooms selected.'}, status=status.HTTP_400_BAD_REQUEST)

        student_idx = 0
        allocated_plans = []
        unallocated_students = []

        with transaction.atomic():
            for room in rooms:
                if student_idx >= total_students:
                    break

                # Ensure Seats exist for the room
                seats = self._ensure_room_seats(room)

                # Filter seats by spacing rule
                if spacing_rule == 'ALTERNATE_COLS':
                    usable_seats = [s for s in seats if s.col_num % 2 == 1 and s.is_usable]
                elif spacing_rule == 'CHECKERBOARD':
                    usable_seats = [s for s in seats if (s.row_num + s.col_num) % 2 == 0 and s.is_usable]
                else:
                    usable_seats = [s for s in seats if s.is_usable]

                # Create or reset SeatingPlan
                plan, _ = SeatingPlan.objects.get_or_create(
                    exam_subject=exam_subject,
                    room=room,
                    defaults={'spacing_rule': spacing_rule}
                )
                plan.allocations.all().delete()

                plan_allocations = []
                for seat in usable_seats:
                    if student_idx < total_students:
                        st = students[student_idx]
                        alloc = SeatAllocation.objects.create(
                            seating_plan=plan,
                            seat=seat,
                            student=st
                        )
                        plan_allocations.append(alloc)
                        student_idx += 1
                    else:
                        break

                plan.total_allocated = len(plan_allocations)
                plan.status = SeatingPlan.Status.GENERATED
                plan.save()
                allocated_plans.append(plan)

            # Check if any students remain unallocated due to room capacity shortage
            if student_idx < total_students:
                for i in range(student_idx, total_students):
                    unallocated_students.append(students[i].roll_no)

        capacity_shortage = len(unallocated_students)
        message = (
            f"Successfully allocated {student_idx}/{total_students} students across {len(allocated_plans)} rooms."
            if capacity_shortage == 0 else
            f"CAPACITY WARNING: Allocated {student_idx}/{total_students} students. Shortage of {capacity_shortage} seats! Please assign more rooms."
        )

        return Response({
            'message': message,
            'total_students': total_students,
            'allocated_count': student_idx,
            'unallocated_count': capacity_shortage,
            'unallocated_rolls': unallocated_students[:20],
            'rooms_used': len(allocated_plans)
        })

    def _ensure_room_seats(self, room):
        seats = list(Seat.objects.filter(room=room).order_by('row_num', 'col_num'))
        if not seats or len(seats) < (room.rows * room.columns):
            Seat.objects.filter(room=room).delete()
            created_seats = []
            for r in range(1, room.rows + 1):
                row_letter = chr(64 + r) if r <= 26 else f"R{r}"
                for c in range(1, room.columns + 1):
                    seat_label = f"{row_letter}{c}"
                    s = Seat(room=room, row_num=r, col_num=c, seat_label=seat_label, is_usable=True)
                    created_seats.append(s)
            Seat.objects.bulk_create(created_seats)
            seats = list(Seat.objects.filter(room=room).order_by('row_num', 'col_num'))
        return seats


class SeatAllocationViewSet(viewsets.ModelViewSet):
    queryset = SeatAllocation.objects.select_related('seating_plan__room', 'seat', 'student').all()
    serializer_class = SeatAllocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        plan_id = self.request.query_params.get('seating_plan')
        student_id = self.request.query_params.get('student')
        if plan_id:
            qs = qs.filter(seating_plan_id=plan_id)
        if student_id:
            qs = qs.filter(student_id=student_id)
        return qs
