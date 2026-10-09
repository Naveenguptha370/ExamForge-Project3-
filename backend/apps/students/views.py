import io
import csv
from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q
from .models import Student, StudentEnrollment, SubjectRegistration, StudentStatus, EligibilityStatus
from .serializers import (
    StudentSerializer, StudentEnrollmentSerializer,
    SubjectRegistrationSerializer
)
from apps.academics.models import Branch, Subject, Semester
from apps.accounts.permissions import IsAdminUserRole, IsStaffOrAdmin

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('register_number')
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['register_number', 'roll_number', 'first_name', 'last_name', 'email', 'branch__name']
    ordering_fields = ['register_number', 'first_name', 'current_semester_number', 'admission_year']

    def get_queryset(self):
        qs = super().get_queryset()
        branch = self.request.query_params.get('branch')
        sem = self.request.query_params.get('semester')
        status_val = self.request.query_params.get('status')
        eligible = self.request.query_params.get('is_eligible')

        if branch:
            qs = qs.filter(branch_id=branch)
        if sem:
            qs = qs.filter(current_semester_number=sem)
        if status_val:
            qs = qs.filter(status=status_val)
        if eligible is not None:
            qs = qs.filter(is_eligible_for_exams=eligible.lower() == 'true')
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        """
        Accepts CSV file or plain CSV text for student records.
        Validates columns, checks for duplicates, and reports invalid rows.
        """
        csv_file = request.FILES.get('file')
        raw_text = request.data.get('csv_content')
        branch_id = request.data.get('branch_id')

        if not csv_file and not raw_text:
            return Response({'success': False, 'message': 'Please provide a CSV file or csv_content string.'}, status=400)

        lines = []
        if csv_file:
            decoded = csv_file.read().decode('utf-8', errors='ignore')
            lines = list(csv.reader(io.StringIO(decoded)))
        elif raw_text:
            lines = list(csv.reader(io.StringIO(raw_text)))

        if not lines:
            return Response({'success': False, 'message': 'CSV content is empty.'}, status=400)

        header = [h.strip().lower() for h in lines[0]]
        expected = ['register_number', 'first_name', 'last_name', 'email', 'branch_code', 'semester']
        
        # Parse rows
        successful_records = []
        invalid_records = []
        duplicates = []

        with transaction.atomic():
            for idx, row in enumerate(lines[1:], start=2):
                if not row or all(c.strip() == '' for c in row):
                    continue
                
                row_dict = {header[i]: row[i].strip() if i < len(row) else '' for i in range(len(header))}
                reg_no = row_dict.get('register_number', '').upper()
                first_name = row_dict.get('first_name', '')
                last_name = row_dict.get('last_name', '')
                email = row_dict.get('email', '')
                branch_code = row_dict.get('branch_code', '')
                sem_str = row_dict.get('semester', '1')

                if not reg_no or not email or not first_name:
                    invalid_records.append({
                        'row': idx,
                        'data': row_dict,
                        'reason': 'Missing mandatory fields (register_number, first_name, email).'
                    })
                    continue

                if Student.objects.filter(Q(register_number=reg_no) | Q(email=email)).exists():
                    duplicates.append({
                        'row': idx,
                        'register_number': reg_no,
                        'email': email,
                        'reason': 'Student with this register number or email already exists.'
                    })
                    continue

                branch_obj = None
                if branch_code:
                    branch_obj = Branch.objects.filter(code__iexact=branch_code).first()
                elif branch_id:
                    branch_obj = Branch.objects.filter(id=branch_id).first()

                if not branch_obj:
                    branch_obj = Branch.objects.first()

                if not branch_obj:
                    invalid_records.append({
                        'row': idx,
                        'data': row_dict,
                        'reason': f"Branch '{branch_code}' not found and no default branch exists."
                    })
                    continue

                try:
                    sem_num = int(sem_str)
                except ValueError:
                    sem_num = 1

                student = Student.objects.create(
                    register_number=reg_no,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=row_dict.get('phone_number', ''),
                    branch=branch_obj,
                    current_semester_number=sem_num,
                    status=StudentStatus.ACTIVE,
                    is_eligible_for_exams=True
                )
                successful_records.append({
                    'id': student.id,
                    'register_number': student.register_number,
                    'name': student.full_name,
                    'branch': branch_obj.code
                })

        return Response({
            'success': True,
            'message': f"Import finished. {len(successful_records)} created, {len(duplicates)} duplicates skipped, {len(invalid_records)} invalid rows.",
            'total_imported': len(successful_records),
            'total_duplicates': len(duplicates),
            'total_invalid': len(invalid_records),
            'successful_records': successful_records,
            'duplicates': duplicates,
            'invalid_records': invalid_records
        })


class SubjectRegistrationViewSet(viewsets.ModelViewSet):
    queryset = SubjectRegistration.objects.all().order_by('student__register_number', 'subject__code')
    serializer_class = SubjectRegistrationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__register_number', 'student__first_name', 'subject__code', 'subject__name']

    def get_queryset(self):
        qs = super().get_queryset()
        student_id = self.request.query_params.get('student')
        subject_id = self.request.query_params.get('subject')
        eligibility = self.request.query_params.get('eligibility_status')
        academic_year = self.request.query_params.get('academic_year')

        if student_id:
            qs = qs.filter(student_id=student_id)
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        if eligibility:
            qs = qs.filter(eligibility_status=eligibility)
        if academic_year:
            qs = qs.filter(academic_year=academic_year)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]
