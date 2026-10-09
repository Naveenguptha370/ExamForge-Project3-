"""
ExamForge M2 — Registration Services Layer
============================================
Business logic isolated from views.
"""
import csv
import io
import uuid
from django.db import transaction
from django.utils import timezone
from django.db.models import Count, Q

from .models import SubjectRegistration, ExamRegistration, BulkRegistrationJob
from academics.models import Subject, AcademicYear, Semester
from students.models import Student


class RegistrationService:
    """Core registration operations."""

    @staticmethod
    def get_available_subjects(student_id):
        """Return subjects available for a student's current semester and department."""
        try:
            student = Student.objects.select_related(
                'department', 'course', 'branch', 'current_semester', 'academic_year'
            ).get(pk=student_id, status='active')
        except Student.DoesNotExist:
            return []

        subjects = Subject.objects.filter(
            status='active',
            department=student.department,
            course=student.course,
        ).select_related('semester', 'department', 'course', 'branch')

        if student.current_semester:
            subjects = subjects.filter(
                Q(semester=student.current_semester) | Q(semester__isnull=True)
            )

        registered_ids = set(
            SubjectRegistration.objects.filter(
                student=student,
                academic_year=student.academic_year,
                status__in=['registered', 'confirmed'],
            ).values_list('subject_id', flat=True)
        )

        result = []
        for sub in subjects:
            d = {
                'id': sub.id,
                'code': sub.code,
                'name': sub.name,
                'subject_type': sub.subject_type,
                'credits': sub.credits,
                'is_external_exam': sub.is_external_exam,
                'is_internal_exam': sub.is_internal_exam,
                'max_external_marks': sub.max_external_marks,
                'max_internal_marks': sub.max_internal_marks,
                'semester': sub.semester.semester_number if sub.semester else None,
                'semester_id': sub.semester_id,
                'already_registered': sub.id in registered_ids,
            }
            result.append(d)
        return result

    @staticmethod
    def get_dashboard_data():
        """Dashboard aggregates for registration module."""
        total_subject = SubjectRegistration.objects.filter(status__in=['registered', 'confirmed']).count()
        total_exam    = ExamRegistration.objects.filter(status__in=['registered', 'confirmed']).count()
        active        = SubjectRegistration.objects.filter(status='registered').count()
        pending_bulk  = BulkRegistrationJob.objects.filter(status__in=['queued', 'processing']).count()

        recent_regs = SubjectRegistration.objects.select_related(
            'student', 'subject', 'academic_year'
        ).filter(status__in=['registered', 'confirmed']).order_by('-created_at')[:10]

        dept_breakdown = (
            SubjectRegistration.objects
            .filter(status__in=['registered', 'confirmed'])
            .values('student__department__code')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return {
            'total_subject_registrations': total_subject,
            'total_exam_registrations':    total_exam,
            'active_registrations':        active,
            'pending_bulk_jobs':           pending_bulk,
            'registrations_by_department': [
                {'department__code': r['student__department__code'], 'count': r['count']}
                for r in dept_breakdown
            ],
            'recent_registrations': [
                {
                    'student_name': r.student_name,
                    'student_roll': r.student_roll,
                    'subject_code': r.subject_code,
                    'subject_name': r.subject_name,
                    'type': 'subject',
                    'status': r.status,
                    'registration_date': str(r.registration_date),
                }
                for r in recent_regs
            ],
        }

    @staticmethod
    def get_summary_report(academic_year_id=None):
        """Top-level summary numbers for the reports page."""
        qs_subj = SubjectRegistration.objects.all()
        qs_exam = ExamRegistration.objects.all()
        if academic_year_id:
            qs_subj = qs_subj.filter(academic_year_id=academic_year_id)
            qs_exam = qs_exam.filter(academic_year_id=academic_year_id)

        by_status = {
            row['status']: row['count']
            for row in qs_subj.values('status').annotate(count=Count('id'))
        }

        return {
            'total_subject':     qs_subj.count(),
            'total_exam':        qs_exam.count(),
            'unique_students':   qs_subj.values('student').distinct().count(),
            'unique_subjects':   qs_subj.values('subject').distinct().count(),
            'by_status':         by_status,
        }

    @staticmethod
    def get_dept_report(academic_year_id=None):
        qs = SubjectRegistration.objects.all()
        if academic_year_id:
            qs = qs.filter(academic_year_id=academic_year_id)
        return list(
            qs.values('student__department__code')
            .annotate(subject_count=Count('id'), unique_students=Count('student', distinct=True))
            .order_by('-subject_count')
        )


class BulkRegistrationService:
    """Handles CSV bulk registration imports."""

    REQUIRED_SUBJECT_COLS = {'student_roll', 'subject_code', 'academic_year'}
    REQUIRED_EXAM_COLS    = {'student_roll', 'subject_code'}

    @classmethod
    @transaction.atomic
    def process_csv(cls, file_obj, registration_type, academic_year_id, created_by=None):
        """
        Parse and process a CSV file for bulk registration.
        Returns a BulkRegistrationJob with results.
        """
        batch_id   = uuid.uuid4()
        file_name  = getattr(file_obj, 'name', 'upload.csv')

        try:
            academic_year = AcademicYear.objects.get(pk=academic_year_id)
        except AcademicYear.DoesNotExist:
            raise ValueError("Invalid academic year ID.")

        job = BulkRegistrationJob.objects.create(
            batch_id=batch_id,
            registration_type=registration_type,
            academic_year=academic_year,
            file_name=file_name,
            status='processing',
            created_by=created_by,
            started_at=timezone.now(),
        )

        content = file_obj.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8-sig')

        reader     = csv.DictReader(io.StringIO(content))
        rows       = list(reader)
        total      = len(rows)
        successful = 0
        failed     = 0
        duplicates = 0
        errors     = []

        required = cls.REQUIRED_EXAM_COLS if registration_type == 'exam' else cls.REQUIRED_SUBJECT_COLS
        headers  = set(reader.fieldnames or [])
        missing  = required - headers
        if missing:
            job.status = 'failed'
            job.error_details = [{'row': 0, 'errors': [{'error': f"Missing columns: {', '.join(missing)}"}]}]
            job.total_rows = total
            job.save()
            return job

        for i, row in enumerate(rows, start=2):
            row_num = i
            row_errors = []
            try:
                roll     = row.get('student_roll', '').strip()
                subj_code = row.get('subject_code', '').strip()

                if not roll:
                    row_errors.append({'error': 'student_roll is required.'})
                if not subj_code:
                    row_errors.append({'error': 'subject_code is required.'})

                if row_errors:
                    errors.append({'row': row_num, 'roll': roll, 'errors': row_errors})
                    failed += 1
                    continue

                try:
                    student = Student.objects.get(roll_number=roll, status='active')
                except Student.DoesNotExist:
                    errors.append({'row': row_num, 'roll': roll, 'errors': [{'error': f"Student '{roll}' not found or inactive."}]})
                    failed += 1
                    continue

                try:
                    subject = Subject.objects.get(code=subj_code, status='active')
                except Subject.DoesNotExist:
                    errors.append({'row': row_num, 'roll': roll, 'errors': [{'error': f"Subject '{subj_code}' not found."}]})
                    failed += 1
                    continue

                if registration_type == 'subject':
                    exists = SubjectRegistration.objects.filter(
                        student=student, subject=subject, academic_year=academic_year,
                        status__in=['registered', 'confirmed']
                    ).exists()
                    if exists:
                        duplicates += 1
                        continue

                    SubjectRegistration.objects.create(
                        student=student, subject=subject,
                        academic_year=academic_year,
                        registered_by=created_by,
                        import_batch_id=batch_id,
                    )
                else:
                    exists = ExamRegistration.objects.filter(
                        student=student, subject=subject, academic_year=academic_year,
                        status__in=['registered', 'confirmed']
                    ).exists()
                    if exists:
                        duplicates += 1
                        continue

                    ExamRegistration.objects.create(
                        student=student, subject=subject,
                        academic_year=academic_year,
                        registered_by=created_by,
                        import_batch_id=batch_id,
                    )

                successful += 1

            except Exception as exc:
                errors.append({'row': row_num, 'roll': row.get('student_roll', '?'), 'errors': [{'error': str(exc)}]})
                failed += 1

        status = 'completed' if failed == 0 and duplicates == 0 else ('partial' if successful > 0 else 'failed')

        job.status          = status
        job.total_rows      = total
        job.successful_rows = successful
        job.failed_rows     = failed
        job.duplicate_rows  = duplicates
        job.error_details   = errors[:200]
        job.completed_at    = timezone.now()
        job.save()

        return job
