import csv
from collections import Counter
import io
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.db.models.functions import Lower
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from apps.academics.models import Department, Course, Branch, Semester

MAX_CSV_SIZE = 5 * 1024 * 1024
MAX_CSV_ROWS = 5000
REQUIRED_CSV_HEADERS = {
    'registration_no',
    'roll_no',
    'first_name',
    'last_name',
    'email',
    'department_code',
    'course_code',
    'semester_number',
}


def _read_student_csv(upload):
    if not upload.name.lower().endswith('.csv'):
        return None, 'Only CSV files are allowed.'
    if upload.size > MAX_CSV_SIZE:
        return None, 'CSV file exceeds the 5 MB upload limit.'

    try:
        content = upload.read().decode('utf-8-sig')
        reader = csv.reader(io.StringIO(content, newline=''), strict=True)
        headers = next(reader, None)
    except (UnicodeDecodeError, csv.Error, StopIteration):
        return None, 'Could not parse the CSV. Please provide a valid UTF-8 CSV file.'

    if not headers or not any(header.strip() for header in headers):
        return None, 'CSV file must contain a header row.'

    normalized_headers = [header.strip().lower() for header in headers]
    if len(normalized_headers) != len(set(normalized_headers)):
        return None, 'CSV file contains duplicate column headers.'

    missing_headers = sorted(REQUIRED_CSV_HEADERS - set(normalized_headers))
    if missing_headers:
        return None, f"Missing required columns: {', '.join(missing_headers)}."

    rows = []
    try:
        for row_number, values in enumerate(reader, start=2):
            if not values or not any(value.strip() for value in values):
                continue
            if len(values) != len(normalized_headers):
                return None, f'Row {row_number}: column count does not match the header.'
            rows.append({
                header: value.strip()
                for header, value in zip(normalized_headers, values)
            })
            if len(rows) > MAX_CSV_ROWS:
                return None, f'CSV file exceeds the {MAX_CSV_ROWS}-row limit.'
    except csv.Error:
        return None, 'Could not parse the CSV. Please check its quoting and delimiters.'

    if not rows:
        return None, 'CSV file contains headers but no student rows.'
    return rows, None


def _validate_student_csv_rows(rows):
    candidate_values = {
        field: {
            row.get(field, '').strip().lower()
            for row in rows
            if row.get(field, '').strip()
        }
        for field in ('registration_no', 'roll_no', 'email')
    }
    existing = {}
    for field, candidates in candidate_values.items():
        existing[field] = set(
            StudentProfile.objects.annotate(normalized_value=Lower(field))
            .filter(normalized_value__in=candidates)
            .values_list('normalized_value', flat=True)
        )
    duplicate_counts = {
        field: Counter(row.get(field, '').strip().lower() for row in rows if row.get(field, '').strip())
        for field in existing
    }
    departments = {item.code.casefold(): item for item in Department.objects.all()}
    courses = {item.code.casefold(): item for item in Course.objects.select_related('department')}
    branches = {item.code.casefold(): item for item in Branch.objects.select_related('course')}
    semesters = list(Semester.objects.all())
    validated_rows = []

    for row_number, row in enumerate(rows, start=2):
        registration_no = row.get('registration_no', '').strip().upper()
        roll_no = row.get('roll_no', '').strip().upper()
        email = row.get('email', '').strip().lower()
        department_code = row.get('department_code', '').strip()
        course_code = row.get('course_code', '').strip()
        branch_code = row.get('branch_code', '').strip()
        first_name = row.get('first_name', '').strip()
        last_name = row.get('last_name', '').strip()
        row_errors = []

        values = {
            'registration_no': registration_no,
            'roll_no': roll_no,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'department_code': department_code,
            'course_code': course_code,
            'semester_number': row.get('semester_number', '').strip(),
        }
        for field, label in (
            ('registration_no', 'Registration number'),
            ('roll_no', 'Roll number'),
            ('first_name', 'First name'),
            ('last_name', 'Last name'),
            ('email', 'Email'),
            ('department_code', 'Department code'),
            ('course_code', 'Course code'),
            ('semester_number', 'Semester number'),
        ):
            if not values[field]:
                row_errors.append(f'{label} is required.')

        for field, label, max_length in (
            ('registration_no', 'Registration number', 30),
            ('roll_no', 'Roll number', 30),
            ('first_name', 'First name', 100),
            ('last_name', 'Last name', 100),
            ('email', 'Email', 254),
        ):
            if values[field] and len(values[field]) > max_length:
                row_errors.append(f'{label} must be at most {max_length} characters.')

        for field, label in (
            ('registration_no', 'Registration number'),
            ('roll_no', 'Roll number'),
            ('email', 'Email'),
        ):
            key = values[field].lower()
            if key and key in existing[field]:
                row_errors.append(f'{label} already exists: {values[field]}.')
            elif key and duplicate_counts[field][key] > 1:
                row_errors.append(f'{label} is duplicated in this CSV: {values[field]}.')

        if email:
            try:
                validate_email(email)
            except ValidationError:
                row_errors.append('Email address is invalid.')

        department = departments.get(department_code.casefold())
        if department_code and not department:
            row_errors.append(f"Department code '{department_code}' was not found.")

        course = courses.get(course_code.casefold())
        if course_code and not course:
            row_errors.append(f"Course code '{course_code}' was not found.")
        elif department and course and course.department_id != department.id:
            row_errors.append('Course does not belong to the selected department.')

        branch = branches.get(branch_code.casefold()) if branch_code else None
        if branch_code and not branch:
            row_errors.append(f"Branch code '{branch_code}' was not found.")
        elif course and branch and branch.course_id != course.id:
            row_errors.append('Branch does not belong to the selected course.')

        semester_number = values['semester_number']
        semester = None
        if semester_number:
            if not semester_number.isdigit() or not 1 <= int(semester_number) <= 8:
                row_errors.append('Semester number must be an integer from 1 to 8.')
            else:
                matches = [
                    item for item in semesters
                    if item.number == int(semester_number)
                ]
                academic_year = row.get('academic_year', '').strip()
                term = row.get('term', '').strip().upper()
                if bool(academic_year) != bool(term):
                    row_errors.append('Provide both academic_year and term to select a semester.')
                elif academic_year and term:
                    matches = [
                        item for item in matches
                        if item.academic_year.casefold() == academic_year.casefold()
                        and item.term == term
                    ]
                if len(matches) == 1:
                    semester = matches[0]
                elif not matches:
                    row_errors.append('The specified semester was not found.')
                else:
                    row_errors.append(
                        'Semester number is ambiguous; include academic_year and term.'
                    )

        phone = row.get('phone', '').strip()
        if len(phone) > 20:
            row_errors.append('Phone must be at most 20 characters.')

        admission_year_text = row.get('admission_year', '').strip()
        if admission_year_text and (
            not admission_year_text.isdigit()
            or len(admission_year_text) != 4
        ):
            row_errors.append('Admission year must be a four-digit year.')
        admission_year = (
            int(admission_year_text)
            if admission_year_text.isdigit() and len(admission_year_text) == 4
            else (int(semester.academic_year[:4]) if semester else 2024)
        )

        validated_rows.append({
            'row': row_number,
            'registration_no': registration_no,
            'roll_no': roll_no,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'department_code': department_code,
            'course_code': course_code,
            'semester_number': semester_number,
            'is_valid': not row_errors,
            'errors': row_errors,
            'student_data': {
                'registration_no': registration_no,
                'roll_no': roll_no,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'department': department,
                'course': course,
                'branch': branch,
                'semester': semester,
                'admission_year': admission_year,
                'contact_phone': phone,
            },
        })

    return validated_rows


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('department', 'course', 'branch', 'semester').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get('department')
        course = self.request.query_params.get('course')
        sem = self.request.query_params.get('semester')
        status_val = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        is_eligible = self.request.query_params.get('is_eligible')

        if dept:
            qs = qs.filter(department_id=dept)
        if course:
            qs = qs.filter(course_id=course)
        if sem:
            qs = qs.filter(semester_id=sem)
        if status_val:
            qs = qs.filter(status=status_val)
        if is_eligible is not None:
            qs = qs.filter(is_eligible_for_exam=is_eligible.lower() == 'true')
        if search:
            qs = qs.filter(
                models.Q(registration_no__icontains=search) |
                models.Q(roll_no__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(email__icontains=search)
            )
        return qs

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total = StudentProfile.objects.count()
        active = StudentProfile.objects.filter(status='ACTIVE').count()
        eligible = StudentProfile.objects.filter(is_eligible_for_exam=True).count()
        return Response({
            'total_students': total,
            'active_students': active,
            'eligible_students': eligible,
            'ineligible_students': total - eligible
        })

    @action(detail=False, methods=['post'])
    def csv_preview(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        rows, error = _read_student_csv(file)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        validated_rows = _validate_student_csv_rows(rows)
        errors = [
            f"Row {row['row']}: {message}"
            for row in validated_rows
            for message in row['errors']
        ]
        invalid_count = sum(not row['is_valid'] for row in validated_rows)
        return Response({
            'total_rows': len(validated_rows),
            'valid_count': len(validated_rows) - invalid_count,
            'invalid_count': invalid_count,
            'preview_rows': [
                {key: value for key, value in row.items() if key != 'student_data'}
                for row in validated_rows[:20]
            ],
            'errors': errors[:50],
        })

    @action(detail=False, methods=['post'])
    def csv_import(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        rows, error = _read_student_csv(file)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        validated_rows = _validate_student_csv_rows(rows)
        errors = [
            f"Row {row['row']}: {message}"
            for row in validated_rows
            for message in row['errors']
        ]
        invalid_count = sum(not row['is_valid'] for row in validated_rows)
        if invalid_count:
            return Response({
                'error': 'Import cancelled because the CSV contains invalid rows. No students were created.',
                'created_count': 0,
                'invalid_count': invalid_count,
                'errors': errors[:50],
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                StudentProfile.objects.bulk_create([
                    StudentProfile(**row['student_data'])
                    for row in validated_rows
                ])
        except IntegrityError:
            return Response({
                'error': 'Import cancelled because a student identifier was added concurrently. No students were created; re-upload and preview the CSV.',
                'created_count': 0,
            }, status=status.HTTP_409_CONFLICT)

        created_count = len(validated_rows)
        return Response({
            'message': f'Successfully imported {created_count} students.',
            'created_count': created_count,
            'skipped_count': 0,
            'errors': [],
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="examforge_students.csv"'
        writer = csv.writer(response)
        writer.writerow(['Registration No', 'Roll No', 'First Name', 'Last Name', 'Email', 'Department', 'Course', 'Semester', 'Status', 'Eligibility'])

        students = self.get_queryset()
        for s in students:
            writer.writerow([
                s.registration_no, s.roll_no, s.first_name, s.last_name, s.email,
                s.department.code, s.course.code, s.semester.number, s.status,
                'ELIGIBLE' if s.is_eligible_for_exam else 'INELIGIBLE'
            ])
        return response
