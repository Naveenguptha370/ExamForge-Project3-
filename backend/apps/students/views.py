import csv
import io
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db import models, transaction
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from apps.academics.models import Department, Course, Branch, Semester

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

        try:
            decoded = file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(decoded))
            rows = []
            errors = []
            row_idx = 1

            existing_regs = set(StudentProfile.objects.values_list('registration_no', flat=True))
            existing_rolls = set(StudentProfile.objects.values_list('roll_no', flat=True))
            existing_emails = set(StudentProfile.objects.values_list('email', flat=True))

            seen_in_file_regs = set()

            for r in reader:
                row_idx += 1
                reg_no = r.get('registration_no', '').strip()
                roll_no = r.get('roll_no', '').strip()
                email = r.get('email', '').strip()
                dept_code = r.get('department_code', '').strip()
                course_code = r.get('course_code', '').strip()
                sem_no = r.get('semester_number', '').strip()

                row_errors = []
                if not reg_no:
                    row_errors.append('Registration number is required')
                elif reg_no in existing_regs or reg_no in seen_in_file_regs:
                    row_errors.append(f'Duplicate registration number: {reg_no}')
                else:
                    seen_in_file_regs.add(reg_no)

                if not roll_no:
                    row_errors.append('Roll number is required')
                elif roll_no in existing_rolls:
                    row_errors.append(f'Duplicate roll number: {roll_no}')

                if not email:
                    row_errors.append('Email is required')
                elif email in existing_emails:
                    row_errors.append(f'Duplicate email: {email}')

                dept = Department.objects.filter(code__iexact=dept_code).first()
                if not dept:
                    row_errors.append(f"Department code '{dept_code}' not found")

                course = Course.objects.filter(code__iexact=course_code).first()
                if not course:
                    row_errors.append(f"Course code '{course_code}' not found")

                sem = Semester.objects.filter(number=sem_no).first() if sem_no.isdigit() else None
                if not sem:
                    row_errors.append(f"Semester '{sem_no}' not found")

                row_info = {
                    'row': row_idx,
                    'registration_no': reg_no,
                    'roll_no': roll_no,
                    'first_name': r.get('first_name', '').strip(),
                    'last_name': r.get('last_name', '').strip(),
                    'email': email,
                    'department_code': dept_code,
                    'course_code': course_code,
                    'semester_number': sem_no,
                    'is_valid': len(row_errors) == 0,
                    'errors': row_errors
                }
                rows.append(row_info)
                if row_errors:
                    errors.extend([f"Row {row_idx}: {err}" for err in row_errors])

            return Response({
                'total_rows': len(rows),
                'valid_count': sum(1 for r in rows if r['is_valid']),
                'invalid_count': sum(1 for r in rows if not r['is_valid']),
                'preview_rows': rows[:20],
                'errors': errors[:50]
            })
        except Exception as e:
            return Response({'error': f'Failed to parse CSV: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def csv_import(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded = file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(decoded))
            created_count = 0
            skipped_count = 0
            errors = []

            with transaction.atomic():
                for idx, r in enumerate(reader, start=2):
                    reg_no = r.get('registration_no', '').strip()
                    roll_no = r.get('roll_no', '').strip()
                    email = r.get('email', '').strip()

                    if StudentProfile.objects.filter(registration_no=reg_no).exists():
                        skipped_count += 1
                        continue

                    dept = Department.objects.filter(code__iexact=r.get('department_code', '').strip()).first()
                    course = Course.objects.filter(code__iexact=r.get('course_code', '').strip()).first()
                    sem_num = r.get('semester_number', '1').strip()
                    sem = Semester.objects.filter(number=int(sem_num) if sem_num.isdigit() else 1).first()

                    if not dept or not course or not sem:
                        errors.append(f"Row {idx}: missing department, course, or semester")
                        continue

                    branch_code = r.get('branch_code', '').strip()
                    branch = Branch.objects.filter(code__iexact=branch_code).first() if branch_code else None

                    StudentProfile.objects.create(
                        registration_no=reg_no,
                        roll_no=roll_no,
                        first_name=r.get('first_name', '').strip(),
                        last_name=r.get('last_name', '').strip(),
                        email=email,
                        department=dept,
                        course=course,
                        branch=branch,
                        semester=sem,
                        admission_year=int(r.get('admission_year', 2024)),
                        contact_phone=r.get('phone', '').strip()
                    )
                    created_count += 1

            return Response({
                'message': f'Successfully imported {created_count} students.',
                'created_count': created_count,
                'skipped_count': skipped_count,
                'errors': errors
            })
        except Exception as e:
            return Response({'error': f'Import failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

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
