from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.db import transaction
from .models import InvigilatorDuty
from .serializers import InvigilatorDutySerializer
from apps.faculty.models import FacultyProfile, FacultyLeave
from apps.seating.models import SeatingPlan

class InvigilatorDutyViewSet(viewsets.ModelViewSet):
    queryset = InvigilatorDuty.objects.select_related(
        'faculty__user', 'faculty__department', 'room__building', 'exam_subject__subject', 'exam_subject__time_slot'
    ).all()
    serializer_class = InvigilatorDutySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        faculty_id = self.request.query_params.get('faculty')
        date = self.request.query_params.get('date')
        session_id = self.request.query_params.get('exam_session')
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if date:
            qs = qs.filter(exam_subject__planned_date=date)
        if session_id:
            qs = qs.filter(exam_subject__exam_session_id=session_id)
        return qs

    @action(detail=False, methods=['post'])
    def auto_allocate(self, request):
        session_id = request.data.get('exam_session_id')
        if not session_id:
            return Response({'error': 'exam_session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all distinct (exam_subject, room) pairs from SeatingPlan for this session
        seating_plans = list(SeatingPlan.objects.filter(
            exam_subject__exam_session_id=session_id
        ).select_related('exam_subject', 'room', 'exam_subject__time_slot'))

        if not seating_plans:
            return Response({'error': 'No seating plans found for this session. Please generate seating plans first.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all available faculty
        faculty_list = list(FacultyProfile.objects.filter(is_available_for_duty=True).select_related('user'))
        if not faculty_list:
            return Response({'error': 'No available faculty members found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Track duties count for fair workload
        duty_counts = {f.id: 0 for f in faculty_list}
        assigned_slots = set()  # (faculty_id, exam_date, slot_id)

        allocated_count = 0
        unstaffed_count = 0

        with transaction.atomic():
            for plan in seating_plans:
                es = plan.exam_subject
                room = plan.room
                date = es.planned_date
                slot_id = es.time_slot_id if es.time_slot else None

                # Check if duty already assigned
                existing = InvigilatorDuty.objects.filter(exam_subject=es, room=room).first()
                if existing:
                    duty_counts[existing.faculty_id] = duty_counts.get(existing.faculty_id, 0) + 1
                    if slot_id:
                        assigned_slots.add((existing.faculty_id, date, slot_id))
                    allocated_count += 1
                    continue

                # Find candidate faculty with minimum duties who are not busy at this date & slot
                # and not on leave
                candidates = []
                for f in faculty_list:
                    if slot_id and (f.id, date, slot_id) in assigned_slots:
                        continue
                    # Check leaves
                    on_leave = FacultyLeave.objects.filter(
                        faculty=f,
                        status='APPROVED',
                        start_date__lte=date,
                        end_date__gte=date
                    ).exists()
                    if on_leave:
                        continue
                    candidates.append(f)

                if candidates:
                    # Pick faculty with lowest duty count
                    candidates.sort(key=lambda f: duty_counts[f.id])
                    chosen = candidates[0]

                    InvigilatorDuty.objects.create(
                        exam_subject=es,
                        room=room,
                        faculty=chosen,
                        duty_role=InvigilatorDuty.DutyRole.HALL_INVIGILATOR,
                        status=InvigilatorDuty.Status.ASSIGNED
                    )
                    duty_counts[chosen.id] += 1
                    if slot_id:
                        assigned_slots.add((chosen.id, date, slot_id))
                    allocated_count += 1
                else:
                    unstaffed_count += 1

        return Response({
            'message': f'Allocated {allocated_count} invigilator duties across {len(seating_plans)} examination halls.',
            'allocated_count': allocated_count,
            'unstaffed_rooms': unstaffed_count,
            'faculty_count': len(faculty_list)
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        session_id = request.request.query_params.get('exam_session') if hasattr(request, 'request') else request.query_params.get('exam_session')
        qs = self.get_queryset()
        total_duties = qs.count()
        confirmed = qs.filter(status='CONFIRMED').count()
        completed = qs.filter(status='COMPLETED').count()

        # Workload per faculty
        workload = list(FacultyProfile.objects.annotate(
            assigned_duties=Count('invigilation_duties')
        ).values('id', 'employee_id', 'user__first_name', 'user__last_name', 'assigned_duties', 'max_duties_per_term'))

        return Response({
            'total_duties': total_duties,
            'confirmed_duties': confirmed,
            'completed_duties': completed,
            'workload': workload
        })
