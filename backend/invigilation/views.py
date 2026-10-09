from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .models import InvigilatorDuty, DutyRequirement
from .serializers import InvigilatorDutySerializer, DutyRequirementSerializer
from .engine import InvigilatorAllocationEngine
from examinations.models import Examination


class InvigilatorDutyViewSet(viewsets.ModelViewSet):
    queryset = InvigilatorDuty.objects.all().select_related(
        'examination', 'examination__subject', 'room', 'room__building', 'faculty', 'faculty__department', 'time_slot'
    ).order_by('duty_date', 'time_slot__start_time', 'room__room_number')
    serializer_class = InvigilatorDutySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        exam_id = self.request.query_params.get('examination')
        room_id = self.request.query_params.get('room')
        faculty_id = self.request.query_params.get('faculty')
        duty_date = self.request.query_params.get('duty_date')

        if exam_id:
            qs = qs.filter(examination_id=exam_id)
        if room_id:
            qs = qs.filter(room_id=room_id)
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if duty_date:
            qs = qs.filter(duty_date=duty_date)
        return qs

    @action(detail=False, methods=['post'])
    def auto_allocate(self, request):
        exam_id = request.data.get('examination_id')
        ratio = request.data.get('ratio_per_students', 30)
        balance = request.data.get('balance_workload', True)

        if not exam_id:
            return Response({'error': 'examination_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = InvigilatorAllocationEngine.allocate(
                int(exam_id),
                ratio_per_students=int(ratio),
                balance_workload=bool(balance)
            )
            return Response(result)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def reassign(self, request):
        duty_id = request.data.get('duty_id')
        new_faculty_id = request.data.get('new_faculty_id')

        if not duty_id or not new_faculty_id:
            return Response({'error': 'duty_id and new_faculty_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = InvigilatorAllocationEngine.reassign_duty(int(duty_id), int(new_faculty_id))
            return Response(result)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def workload(self, request):
        data = InvigilatorAllocationEngine.get_faculty_workload_stats()
        return Response(data)

    @action(detail=False, methods=['get'])
    def printable_roster(self, request):
        exam_id = request.query_params.get('examination_id')
        if not exam_id:
            return Response({'error': 'examination_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        exam = Examination.objects.select_related('subject', 'session', 'time_slot').get(id=exam_id)
        duties = InvigilatorDuty.objects.filter(examination=exam).select_related('faculty', 'faculty__department', 'room', 'room__building')

        roster = [
            {
                'sno': idx + 1,
                'faculty_name': d.faculty.name,
                'employee_id': d.faculty.employee_id,
                'department': d.faculty.department.name,
                'room_number': d.room.room_number,
                'building_name': d.room.building.name,
                'role': d.get_role_display(),
                'phone': d.faculty.phone,
                'email': d.faculty.email,
                'status': d.status
            }
            for idx, d in enumerate(duties)
        ]

        return Response({
            'session_name': exam.session.name,
            'subject_code': exam.subject.code,
            'subject_name': exam.subject.name,
            'exam_date': exam.exam_date,
            'time_slot': exam.time_slot.name,
            'total_invigilators': len(roster),
            'roster': roster
        })


class DutyRequirementViewSet(viewsets.ModelViewSet):
    queryset = DutyRequirement.objects.all().select_related('examination', 'room', 'examination__subject', 'room__building')
    serializer_class = DutyRequirementSerializer
