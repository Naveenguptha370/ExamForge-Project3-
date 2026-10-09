import csv
import io
from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Timetable, TimetableEntry, SchedulingClash, TimetableRevision, TimetableStatus
from .serializers import (
    TimetableSerializer, TimetableDetailSerializer,
    TimetableEntrySerializer, SchedulingClashSerializer,
    TimetableRevisionSerializer
)
from .engine.solver import ConstraintTimetableSolver, SolverOutcome
from .engine.conflict_analyzer import ConflictAnalyzer
from .engine.pdf_exporter import generate_timetable_pdf
from apps.examinations.models import ExamSession, TimeSlot, ExamSubjectConfig
from apps.accounts.permissions import IsStaffOrAdmin, IsAdminUserRole

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all().order_by('-created_at')
    serializer_class = TimetableSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['session__name', 'session__code', 'version']

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return TimetableDetailSerializer
        return TimetableSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate', 'manual_override']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        """
        Executes the CSP Constraint Solver for the given session_id.
        """
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'success': False, 'message': 'session_id is required.'}, status=400)

        session = get_object_or_404(ExamSession, id=session_id)
        if session.is_locked and not (request.user.role == 'ADMIN' or request.user.is_superuser):
            return Response({'success': False, 'message': 'This session is locked (Approved or Published).'}, status=400)

        solver = ConstraintTimetableSolver(exam_session=session, user=request.user)
        result = solver.solve()

        return Response({
            'success': result.outcome in [SolverOutcome.SUCCESS, SolverOutcome.PARTIAL],
            'result': result.to_dict(),
            'timetable': TimetableDetailSerializer(result.timetable).data if result.timetable else None
        })

    @action(detail=True, methods=['post'], url_path='revalidate')
    def revalidate(self, request, pk=None):
        """
        Runs the ConflictAnalyzer on an existing timetable to recalculate hard/soft clashes.
        """
        timetable = self.get_object()
        analyzer = ConflictAnalyzer(timetable)
        audit_result = analyzer.analyze()

        return Response({
            'success': True,
            'message': 'Timetable conflict audit completed.',
            'audit': {
                'is_conflict_free': audit_result['is_conflict_free'],
                'clash_count': audit_result['clash_count'],
                'critical_count': audit_result['critical_count'],
                'high_count': audit_result['high_count'],
                'medium_count': audit_result['medium_count']
            },
            'timetable': TimetableSerializer(timetable).data
        })

    @action(detail=True, methods=['post'], url_path='manual-override')
    def manual_override(self, request, pk=None):
        """
        Allows an administrator or exam staff to reschedule a specific subject to a new date and slot,
        then automatically live-revalidates conflicts and records a revision log.
        """
        timetable = self.get_object()
        if timetable.status == 'PUBLISHED' and not (request.user.role == 'ADMIN' or request.user.is_superuser):
            return Response({'success': False, 'message': 'Only Administrator can modify a published timetable.'}, status=403)

        entry_id = request.data.get('entry_id')
        new_date_str = request.data.get('exam_date')
        new_slot_id = request.data.get('time_slot_id')

        if not entry_id or not new_date_str or not new_slot_id:
            return Response({'success': False, 'message': 'entry_id, exam_date, and time_slot_id are required.'}, status=400)

        entry = get_object_or_404(TimetableEntry, id=entry_id, timetable=timetable)
        new_slot = get_object_or_404(TimeSlot, id=new_slot_id)

        old_date = entry.exam_date
        old_slot = entry.time_slot

        entry.exam_date = new_date_str
        entry.time_slot = new_slot
        entry.is_manual_override = True
        entry.save()

        # Update version string (e.g. 1.0 -> 1.1)
        try:
            parts = timetable.version.split('.')
            new_minor = int(parts[1]) + 1
            timetable.version = f"{parts[0]}.{new_minor}"
        except Exception:
            timetable.version = f"{timetable.version}.1"

        timetable.save()

        # Record revision history
        subj = entry.subject_config.subject
        TimetableRevision.objects.create(
            timetable=timetable,
            revision_number=timetable.version,
            author=request.user,
            change_summary=f"Manual Override: Rescheduled {subj.code} from {old_date} ({old_slot.name}) to {new_date_str} ({new_slot.name}).",
            diff_payload={
                'subject': subj.code,
                'from_date': str(old_date),
                'from_slot': old_slot.name,
                'to_date': str(new_date_str),
                'to_slot': new_slot.name
            }
        )

        # Live revalidate
        analyzer = ConflictAnalyzer(timetable)
        analyzer.analyze()

        return Response({
            'success': True,
            'message': f"Rescheduled {subj.code} successfully. Revalidation completed.",
            'timetable': TimetableDetailSerializer(timetable).data
        })

    @action(detail=True, methods=['get'], url_path='export-pdf')
    def export_pdf(self, request, pk=None):
        """
        Streams down a beautifully styled ReportLab PDF timetable.
        """
        timetable = self.get_object()
        dept_id = request.query_params.get('department')
        branch_id = request.query_params.get('branch')

        pdf_bytes = generate_timetable_pdf(timetable, department_id=dept_id, branch_id=branch_id)
        
        filename = f"Timetable_{timetable.session.code}_v{timetable.version}.pdf"
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=True, methods=['get'], url_path='export-csv')
    def export_csv(self, request, pk=None):
        """
        Exports the timetable as a clean CSV file.
        """
        timetable = self.get_object()
        entries = timetable.entries.select_related(
            'subject_config__subject',
            'subject_config__subject__department',
            'subject_config__subject__branch',
            'time_slot'
        ).order_by('exam_date', 'time_slot__start_time')

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Exam Date', 'Day', 'Time Slot', 'Shift', 'Start Time', 'End Time',
            'Subject Code', 'Subject Title', 'Department', 'Branch',
            'Semester', 'Credits', 'Expected Students', 'QP Code'
        ])

        for e in entries:
            s = e.subject_config.subject
            writer.writerow([
                e.exam_date,
                e.exam_date.strftime('%A'),
                e.time_slot.name,
                e.time_slot.get_shift_display(),
                e.time_slot.start_time.strftime('%I:%M %p'),
                e.time_slot.end_time.strftime('%I:%M %p'),
                s.code,
                s.name,
                s.department.name if s.department else '',
                s.branch.name if s.branch else '',
                s.semester_number,
                s.credits,
                e.expected_students,
                e.subject_config.question_paper_code
            ])

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Timetable_{timetable.session.code}.csv"'
        return response


class TimetableEntryViewSet(viewsets.ModelViewSet):
    queryset = TimetableEntry.objects.all().order_by('exam_date', 'time_slot__start_time')
    serializer_class = TimetableEntrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject_config__subject__code', 'subject_config__subject__name']

    def get_queryset(self):
        qs = super().get_queryset()
        timetable_id = self.request.query_params.get('timetable')
        dept_id = self.request.query_params.get('department')
        branch_id = self.request.query_params.get('branch')
        sem = self.request.query_params.get('semester')
        date = self.request.query_params.get('date')

        if timetable_id:
            qs = qs.filter(timetable_id=timetable_id)
        if dept_id:
            qs = qs.filter(subject_config__subject__department_id=dept_id)
        if branch_id:
            qs = qs.filter(subject_config__subject__branch_id=branch_id)
        if sem:
            qs = qs.filter(subject_config__subject__semester_number=sem)
        if date:
            qs = qs.filter(exam_date=date)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]


class SchedulingClashViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchedulingClash.objects.all().order_by('-severity', 'exam_date')
    serializer_class = SchedulingClashSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        timetable_id = self.request.query_params.get('timetable')
        severity = self.request.query_params.get('severity')
        clash_type = self.request.query_params.get('clash_type')

        if timetable_id:
            qs = qs.filter(timetable_id=timetable_id)
        if severity:
            qs = qs.filter(severity=severity)
        if clash_type:
            qs = qs.filter(clash_type=clash_type)
        return qs


class TimetableRevisionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TimetableRevision.objects.all().order_by('-created_at')
    serializer_class = TimetableRevisionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        timetable_id = self.request.query_params.get('timetable')
        if timetable_id:
            qs = qs.filter(timetable_id=timetable_id)
        return qs
