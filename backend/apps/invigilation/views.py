from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import InvigilatorDuty, DutyStatus, DutyRole
from .serializers import InvigilatorDutySerializer
from apps.examinations.models import ExamSession, TimeSlot
from apps.faculty.models import FacultyProfile, FacultyAvailability
from apps.seating.models import SeatingPlan, RoomAllocation
from apps.accounts.permissions import IsStaffOrAdmin

class InvigilatorDutyViewSet(viewsets.ModelViewSet):
    queryset = InvigilatorDuty.objects.all().order_by('exam_date', 'time_slot__start_time')
    serializer_class = InvigilatorDutySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['faculty__first_name', 'faculty__last_name', 'faculty__employee_id', 'room__room_number']

    def get_queryset(self):
        qs = super().get_queryset()
        session_id = self.request.query_params.get('session')
        faculty_id = self.request.query_params.get('faculty')
        date = self.request.query_params.get('date')

        if session_id:
            qs = qs.filter(session_id=session_id)
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if date:
            qs = qs.filter(exam_date=date)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'auto_assign']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='auto-assign')
    def auto_assign(self, request):
        """
        Fairly distributes invigilation duties to available faculty members
        for all active room allocations in the specified session.
        """
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'success': False, 'message': 'session_id is required.'}, status=400)

        session = ExamSession.objects.get(id=session_id)
        plans = SeatingPlan.objects.filter(session=session).prefetch_related('room_allocations__room')

        if not plans.exists():
            return Response({'success': False, 'message': 'No seating plans created yet for this session. Generate seating plans first.'}, status=400)

        faculty_list = list(FacultyProfile.objects.filter(
            status='ACTIVE',
            is_eligible_for_invigilation=True
        ).order_by('current_duties_count'))

        if not faculty_list:
            return Response({'success': False, 'message': 'No active eligible faculty found.'}, status=400)

        assigned_count = 0
        faculty_pointer = 0

        with transaction.atomic():
            for plan in plans:
                for alloc in plan.room_allocations.all():
                    # Check if already assigned
                    if alloc.primary_invigilator:
                        continue

                    # Pick next available faculty
                    tries = 0
                    assigned_fac = None

                    while tries < len(faculty_list):
                        candidate = faculty_list[faculty_pointer % len(faculty_list)]
                        faculty_pointer += 1
                        tries += 1

                        # Check if already has duty on same slot
                        existing_duty = InvigilatorDuty.objects.filter(
                            faculty=candidate,
                            exam_date=plan.exam_date,
                            time_slot=plan.time_slot
                        ).exists()

                        if not existing_duty:
                            assigned_fac = candidate
                            break

                    if assigned_fac:
                        duty = InvigilatorDuty.objects.create(
                            session=session,
                            faculty=assigned_fac,
                            room=alloc.room,
                            exam_date=plan.exam_date,
                            time_slot=plan.time_slot,
                            duty_role=DutyRole.HALL_INVIGILATOR,
                            status=DutyStatus.ASSIGNED
                        )
                        alloc.primary_invigilator = assigned_fac
                        alloc.save()
                        
                        assigned_fac.current_duties_count += 1
                        assigned_fac.save()
                        assigned_count += 1

        return Response({
            'success': True,
            'message': f"Assigned {assigned_count} invigilation duties with balanced faculty workload.",
            'total_assigned': assigned_count
        })
