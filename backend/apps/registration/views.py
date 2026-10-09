from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import StudentEnrollment, SubjectRegistration
from .serializers import StudentEnrollmentSerializer, SubjectRegistrationSerializer

class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.select_related('student', 'semester').all()
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get('student')
        sem = self.request.query_params.get('semester')
        year = self.request.query_params.get('academic_year')
        if student:
            qs = qs.filter(student_id=student)
        if sem:
            qs = qs.filter(semester_id=sem)
        if year:
            qs = qs.filter(academic_year=year)
        return qs


class SubjectRegistrationViewSet(viewsets.ModelViewSet):
    queryset = SubjectRegistration.objects.select_related('student', 'subject', 'semester').all()
    serializer_class = SubjectRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get('student')
        subject = self.request.query_params.get('subject')
        sem = self.request.query_params.get('semester')
        eligibility = self.request.query_params.get('eligibility_status')
        if student:
            qs = qs.filter(student_id=student)
        if subject:
            qs = qs.filter(subject_id=subject)
        if sem:
            qs = qs.filter(semester_id=sem)
        if eligibility:
            qs = qs.filter(eligibility_status=eligibility)
        return qs

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total = SubjectRegistration.objects.count()
        eligible = SubjectRegistration.objects.filter(eligibility_status='ELIGIBLE').count()
        shortage = SubjectRegistration.objects.filter(eligibility_status='ATTENDANCE_SHORTAGE').count()
        fees_due = SubjectRegistration.objects.filter(eligibility_status='FEES_DUE').count()
        return Response({
            'total_registrations': total,
            'eligible_registrations': eligible,
            'attendance_shortage': shortage,
            'fees_due': fees_due,
            'other_ineligible': total - (eligible + shortage + fees_due)
        })
