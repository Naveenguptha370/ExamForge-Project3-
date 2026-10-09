from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import AttendanceRecord, ExamAttendanceStatus
from .serializers import AttendanceRecordSerializer
from apps.scheduling.models import TimetableEntry
from apps.students.models import Student, SubjectRegistration, EligibilityStatus
from apps.accounts.permissions import IsStaffOrAdmin

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all().order_by('student__register_number')
    serializer_class = AttendanceRecordSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['student__register_number', 'student__first_name', 'student__last_name', 'answer_booklet_number']

    def get_queryset(self):
        qs = super().get_queryset()
        entry_id = self.request.query_params.get('entry')
        session_id = self.request.query_params.get('session')
        status_val = self.request.query_params.get('status')
        room_id = self.request.query_params.get('room')

        if entry_id:
            qs = qs.filter(timetable_entry_id=entry_id)
        if session_id:
            qs = qs.filter(session_id=session_id)
        if status_val:
            qs = qs.filter(status=status_val)
        if room_id:
            qs = qs.filter(room_id=room_id)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'mark_bulk']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='mark-bulk')
    def mark_bulk(self, request):
        """
        Batch-updates attendance records for a room or examination entry.
        """
        records_data = request.data.get('records', [])
        if not records_data:
            return Response({'success': False, 'message': 'records array is required.'}, status=400)

        updated = 0
        with transaction.atomic():
            for item in records_data:
                rec_id = item.get('id')
                status_val = item.get('status', ExamAttendanceStatus.PRESENT)
                booklet = item.get('answer_booklet_number', '')
                remarks = item.get('remarks', '')

                if rec_id:
                    rec = AttendanceRecord.objects.filter(id=rec_id).first()
                    if rec:
                        rec.status = status_val
                        if booklet:
                            rec.answer_booklet_number = booklet
                        if remarks:
                            rec.remarks = remarks
                        rec.recorded_by = request.user
                        rec.save()
                        updated += 1

        return Response({'success': True, 'message': f'Successfully updated {updated} attendance records.'})
