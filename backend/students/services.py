"""
ExamForge M2 — Student Management Service Layer
=================================================
All business logic for student operations is isolated here.
Views call services; services interact with models.

This separation keeps views thin and makes logic testable in isolation.
"""

import csv
import io
import logging
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any

from django.db import transaction, IntegrityError
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Count, Q

from students.models import (
    Student,
    StudentImportLog,
    EnrollmentRecord,
    StudentStatusChoices,
)
from academics.models import (
    Department,
    Course,
    Branch,
    Semester,
    AcademicYear,
    StatusChoices,
)

logger = logging.getLogger(__name__)

# ─── Import Column Configuration ─────────────────────────────────────────────────
REQUIRED_IMPORT_COLUMNS = settings.STUDENT_IMPORT['REQUIRED_COLUMNS']
OPTIONAL_IMPORT_COLUMNS = settings.STUDENT_IMPORT['OPTIONAL_COLUMNS']
ALL_IMPORT_COLUMNS = REQUIRED_IMPORT_COLUMNS + OPTIONAL_IMPORT_COLUMNS
MAX_IMPORT_ROWS = settings.STUDENT_IMPORT['MAX_ROWS']
IMPORT_BATCH_SIZE = settings.STUDENT_IMPORT['BATCH_SIZE']


class StudentService:
    """
    Encapsulates all student management business logic.
    All public methods are safe to call from views.
    """

    @staticmethod
    def get_dashboard_stats(user) -> Dict[str, Any]:
        """
        Compute real database statistics for the student dashboard.
        Respects user role — admins see all, faculty see only their department.
        """
        base_qs = Student.objects.all()

        # Role-based filtering (integrate with M1 roles)
        if hasattr(user, 'role') and user.role == 'faculty':
            faculty_dept = getattr(user, 'department_id', None)
            if faculty_dept:
                base_qs = base_qs.filter(department_id=faculty_dept)

        total = base_qs.count()
        active = base_qs.filter(status=StudentStatusChoices.ACTIVE).count()
        inactive = base_qs.filter(status=StudentStatusChoices.INACTIVE).count()
        graduated = base_qs.filter(status=StudentStatusChoices.GRADUATED).count()
        exam_eligible = base_qs.filter(
            status=StudentStatusChoices.ACTIVE,
            is_eligible_for_exam=True
        ).count()

        # Students by department
        by_dept = list(
            base_qs.values('department__code', 'department__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Students by semester
        by_sem = list(
            base_qs.filter(status=StudentStatusChoices.ACTIVE)
            .values('current_semester__semester_number', 'course__code')
            .annotate(count=Count('id'))
            .order_by('current_semester__semester_number')[:20]
        )

        # Students by course
        by_course = list(
            base_qs.values('course__code', 'course__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Recent enrollments (last 10)
        recent = list(
            base_qs.order_by('-created_at')[:10].values(
                'student_id', 'roll_number', 'full_name',
                'department__code', 'course__code', 'created_at',
            )
        )

        # This year enrollments
        current_year = timezone.now().year
        this_year = base_qs.filter(admission_year=current_year).count()

        # Pending import logs
        pending_imports = StudentImportLog.objects.filter(
            status__in=['pending', 'processing']
        ).count()

        return {
            'total_students': total,
            'active_students': active,
            'inactive_students': inactive,
            'graduated_students': graduated,
            'exam_eligible_students': exam_eligible,
            'students_by_department': by_dept,
            'students_by_semester': by_sem,
            'students_by_course': by_course,
            'recent_enrollments': recent,
            'this_year_enrollments': this_year,
            'import_logs_pending': pending_imports,
        }

    @staticmethod
    def validate_csv_file(file) -> Tuple[bool, str, Optional[List[Dict]]]:
        """
        Validates an uploaded CSV file before processing.
        Returns: (is_valid, error_message, rows_or_none)
        """
        # Check file size
        max_size = settings.MAX_UPLOAD_SIZE
        if file.size > max_size:
            return False, f'File size exceeds maximum of {max_size // (1024*1024)} MB.', None

        # Check file extension
        name = file.name.lower()
        if not name.endswith('.csv'):
            return False, 'Only CSV files (.csv) are allowed.', None

        # Read and parse
        try:
            content = file.read().decode('utf-8-sig')  # Handle BOM
        except UnicodeDecodeError:
            try:
                file.seek(0)
                content = file.read().decode('latin-1')
            except Exception:
                return False, 'Could not decode file. Please ensure it is UTF-8 encoded.', None

        if not content.strip():
            return False, 'The uploaded file is empty.', None

        reader = csv.DictReader(io.StringIO(content))

        # Validate headers
        if not reader.fieldnames:
            return False, 'CSV file has no headers.', None

        headers = [h.strip().lower() for h in reader.fieldnames]
        missing = [col for col in REQUIRED_IMPORT_COLUMNS if col not in headers]
        if missing:
            return False, f'Missing required columns: {", ".join(missing)}.', None

        rows = list(reader)
        if not rows:
            return False, 'CSV file has headers but no data rows.', None

        if len(rows) > MAX_IMPORT_ROWS:
            return False, (
                f'CSV file has {len(rows)} rows. Maximum allowed is {MAX_IMPORT_ROWS}.'
            ), None

        return True, '', rows

    @staticmethod
    @transaction.atomic
    def process_student_import(
        rows: List[Dict],
        academic_year: AcademicYear,
        imported_by,
        file_name: str = 'import.csv',
    ) -> StudentImportLog:
        """
        Process a validated list of CSV rows and create student records.

        - Validates each row individually.
        - Detects duplicates within the file and against the database.
        - Creates students in batches.
        - Returns a complete ImportLog with row-level results.

        This entire operation runs in a transaction. If a critical error
        occurs, all changes are rolled back.
        """
        log = StudentImportLog.objects.create(
            imported_by=imported_by,
            file_name=file_name,
            status=StudentImportLog.ImportStatusChoices.PROCESSING,
            total_rows=len(rows),
            academic_year=academic_year,
        )

        successful = 0
        failed = 0
        duplicates = 0
        skipped = 0
        error_details = []

        # Pre-load lookup caches to avoid repeated DB hits
        dept_cache = {d.code.upper(): d for d in Department.objects.filter(status=StatusChoices.ACTIVE)}
        course_cache = {f'{c.department.code.upper()}:{c.code.upper()}': c for c in Course.objects.filter(status=StatusChoices.ACTIVE).select_related('department')}
        branch_cache = {f'{b.course.code.upper()}:{b.code.upper()}': b for b in Branch.objects.filter(status=StatusChoices.ACTIVE).select_related('course')}

        # Track roll numbers and emails seen in this import to detect in-file duplicates
        seen_rolls = set()
        seen_emails = set()

        students_to_create = []

        for row_num, row in enumerate(rows, start=2):  # start=2 because row 1 is header
            row_errors = []

            try:
                # Clean and extract values
                roll = row.get('roll_number', '').strip().upper()
                name = row.get('full_name', '').strip()
                email = row.get('email', '').strip().lower()
                dept_code = row.get('department_code', '').strip().upper()
                course_code = row.get('course_code', '').strip().upper()
                branch_code = row.get('branch_code', '').strip().upper()
                sem_num_str = row.get('semester_number', '').strip()
                ay_label = row.get('academic_year', '').strip()
                phone = row.get('phone', '').strip()
                gender = row.get('gender', '').strip().lower()

                # Required field validation
                if not roll:
                    row_errors.append({'field': 'roll_number', 'error': 'Roll number is required.'})
                if not name:
                    row_errors.append({'field': 'full_name', 'error': 'Full name is required.'})
                if not email:
                    row_errors.append({'field': 'email', 'error': 'Email is required.'})
                if not dept_code:
                    row_errors.append({'field': 'department_code', 'error': 'Department code is required.'})
                if not course_code:
                    row_errors.append({'field': 'course_code', 'error': 'Course code is required.'})
                if not sem_num_str:
                    row_errors.append({'field': 'semester_number', 'error': 'Semester number is required.'})
                if not ay_label:
                    row_errors.append({'field': 'academic_year', 'error': 'Academic year is required.'})

                if row_errors:
                    error_details.append({'row': row_num, 'roll': roll or '?', 'errors': row_errors})
                    failed += 1
                    continue

                # In-file duplicate check
                if roll in seen_rolls:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'roll_number', 'error': f'Duplicate roll number "{roll}" within the import file.'}]
                    })
                    duplicates += 1
                    continue
                if email in seen_emails:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'email', 'error': f'Duplicate email "{email}" within the import file.'}]
                    })
                    duplicates += 1
                    continue

                # Database duplicate check
                if Student.objects.filter(roll_number=roll).exists():
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'roll_number', 'error': f'Student with roll number "{roll}" already exists in the database.'}]
                    })
                    duplicates += 1
                    continue
                if Student.objects.filter(institutional_email=email).exists():
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'email', 'error': f'Student with email "{email}" already exists in the database.'}]
                    })
                    duplicates += 1
                    continue

                # Resolve academic relationships
                dept = dept_cache.get(dept_code)
                if not dept:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'department_code', 'error': f'Department "{dept_code}" not found or inactive.'}]
                    })
                    failed += 1
                    continue

                course_key = f'{dept_code}:{course_code}'
                course = course_cache.get(course_key)
                if not course:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'course_code', 'error': f'Course "{course_code}" not found in department "{dept_code}" or inactive.'}]
                    })
                    failed += 1
                    continue

                branch = None
                if branch_code:
                    branch_key = f'{course_code}:{branch_code}'
                    branch = branch_cache.get(branch_key)
                    if not branch:
                        error_details.append({
                            'row': row_num, 'roll': roll,
                            'errors': [{'field': 'branch_code', 'error': f'Branch "{branch_code}" not found in course "{course_code}".'}]
                        })
                        failed += 1
                        continue

                # Parse semester number
                try:
                    sem_num = int(sem_num_str)
                except ValueError:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'semester_number', 'error': 'Semester number must be a valid integer.'}]
                    })
                    failed += 1
                    continue

                # Find semester
                sem_qs = Semester.objects.filter(
                    course=course,
                    semester_number=sem_num,
                    status=StatusChoices.ACTIVE,
                )
                if branch:
                    sem_qs = sem_qs.filter(Q(branch=branch) | Q(branch__isnull=True))
                semester = sem_qs.first()
                if not semester:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'semester_number', 'error': f'Semester {sem_num} not found for course "{course_code}".'}]
                    })
                    failed += 1
                    continue

                # Resolve academic year
                try:
                    acad_year = AcademicYear.objects.get(label=ay_label)
                except AcademicYear.DoesNotExist:
                    error_details.append({
                        'row': row_num, 'roll': roll,
                        'errors': [{'field': 'academic_year', 'error': f'Academic year "{ay_label}" not found.'}]
                    })
                    failed += 1
                    continue

                # Parse admission year from academic year label
                try:
                    admission_year = int(ay_label.split('-')[0])
                except (ValueError, IndexError):
                    admission_year = timezone.now().year

                # Validate gender
                valid_genders = ['male', 'female', 'other', 'prefer_not_to_say', '']
                if gender and gender not in valid_genders:
                    gender = 'prefer_not_to_say'

                # Build student instance (don't save yet — batch later)
                student_id = StudentService._generate_student_id_for_import(
                    dept_code, admission_year, successful
                )

                student = Student(
                    student_id=student_id,
                    roll_number=roll,
                    full_name=name,
                    institutional_email=email,
                    phone=phone or '',
                    department=dept,
                    course=course,
                    branch=branch,
                    current_semester=semester,
                    academic_year=acad_year,
                    admission_year=admission_year,
                    gender=gender or 'prefer_not_to_say',
                    status=StudentStatusChoices.ACTIVE,
                    created_by=imported_by,
                    updated_by=imported_by,
                )

                seen_rolls.add(roll)
                seen_emails.add(email)
                students_to_create.append(student)
                successful += 1

            except Exception as exc:
                logger.exception('Unexpected error processing row %d: %s', row_num, exc)
                error_details.append({
                    'row': row_num, 'roll': row.get('roll_number', '?'),
                    'errors': [{'field': 'general', 'error': f'Unexpected error: {str(exc)}'}]
                })
                failed += 1

        # Batch-insert all valid students
        if students_to_create:
            try:
                Student.objects.bulk_create(students_to_create, batch_size=IMPORT_BATCH_SIZE)
            except IntegrityError as exc:
                logger.error('Bulk create failed: %s', exc)
                # In case of integrity error, fall back to individual inserts with error capture
                successful = 0
                for student in students_to_create:
                    try:
                        student.save()
                        successful += 1
                    except IntegrityError as ie:
                        error_details.append({
                            'row': '-',
                            'roll': student.roll_number,
                            'errors': [{'field': 'general', 'error': str(ie)}]
                        })
                        failed += 1

        # Update import log
        log.successful_rows = successful
        log.failed_rows = failed
        log.duplicate_rows = duplicates
        log.skipped_rows = skipped
        log.error_details = error_details
        log.summary = (
            f'Import completed: {successful} created, {failed} failed, '
            f'{duplicates} duplicates, {skipped} skipped out of {len(rows)} rows.'
        )

        if failed == 0 and duplicates == 0:
            log.mark_completed()
        else:
            log.mark_partial()

        logger.info(
            'Import complete: %s created, %s failed, %s duplicates',
            successful, failed, duplicates
        )
        return log

    @staticmethod
    def _generate_student_id_for_import(dept_code: str, admission_year: int, seq: int) -> str:
        year_suffix = str(admission_year)[-2:]
        return f'{dept_code}-{year_suffix}-{(seq + 1):04d}-I'

    @staticmethod
    def get_csv_template_content() -> str:
        """Return the downloadable CSV import template content."""
        headers = REQUIRED_IMPORT_COLUMNS + OPTIONAL_IMPORT_COLUMNS
        example_row = [
            'CSE2024001',      # roll_number
            'Jane Doe',        # full_name
            'jane@college.edu', # email
            'CSE',             # department_code
            'BTECH',           # course_code
            'CSE',             # branch_code
            '3',               # semester_number
            '2024-2025',       # academic_year
            '9876543210',      # phone (optional)
            '2024-06-01',      # admission_date (optional)
            'female',          # gender (optional)
            '2004-05-15',      # date_of_birth (optional)
        ]
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerow(example_row)
        return output.getvalue()

    @staticmethod
    def deactivate_student(student_id: str, reason: str, user) -> Student:
        """Deactivate a student with audit logging."""
        student = Student.objects.get(pk=student_id)
        student.deactivate(reason=reason, user=user)
        return student

    @staticmethod
    def get_student_summary(student_id: str) -> Dict[str, Any]:
        """Return a comprehensive summary of a student's academic activity."""
        student = Student.objects.select_related(
            'department', 'course', 'branch',
            'current_semester', 'academic_year',
        ).get(pk=student_id)

        subject_regs = student.subject_registrations.filter(
            status='registered'
        ).select_related('subject').count()

        exam_regs = student.exam_registrations.filter(
            status='registered'
        ).count()

        enrollment_history = list(
            student.enrollment_records.select_related(
                'semester', 'academic_year'
            ).order_by('-enrolled_date').values(
                'semester__semester_number',
                'academic_year__label',
                'status',
                'enrolled_date',
            )
        )

        can_register, reason = student.can_register_for_exam()

        return {
            'student': student,
            'subject_registrations_count': subject_regs,
            'exam_registrations_count': exam_regs,
            'enrollment_history': enrollment_history,
            'can_register_for_exam': can_register,
            'eligibility_reason': reason,
        }
