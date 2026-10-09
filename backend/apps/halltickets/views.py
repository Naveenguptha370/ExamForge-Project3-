import uuid
from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from .models import HallTicket
from .serializers import HallTicketSerializer
from .pdf_generator import generate_hall_ticket_pdf
from apps.examinations.models import ExamSession
from apps.students.models import Student, EligibilityStatus
from apps.accounts.permissions import IsStaffOrAdmin

class HallTicketViewSet(viewsets.ModelViewSet):
    queryset = HallTicket.objects.all().order_by('student__register_number')
    serializer_class = HallTicketSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['ticket_number', 'student__register_number', 'student__first_name', 'student__last_name']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user.role == 'STUDENT' and hasattr(user, 'student_profile'):
            return qs.filter(student=user.student_profile)
        session_id = self.request.query_params.get('session')
        student_id = self.request.query_params.get('student')
        if session_id:
            qs = qs.filter(session_id=session_id)
        if student_id:
            qs = qs.filter(student_id=student_id)
        return qs

    def get_permissions(self):
        if self.action in ['generate_bulk', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='generate-bulk')
    def generate_bulk(self, request):
        """
        Generates Hall Tickets in bulk for all eligible students in a published exam session.
        """
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'success': False, 'message': 'session_id is required.'}, status=400)

        session = ExamSession.objects.get(id=session_id)
        if not session.is_published and not (request.user.role == 'ADMIN' or request.user.is_superuser):
            return Response({'success': False, 'message': 'Hall tickets can only be generated for published examination sessions.'}, status=400)

        students = Student.objects.filter(is_eligible_for_exams=True, status='ACTIVE')
        created_count = 0

        with transaction.atomic():
            for idx, student in enumerate(students, start=1):
                ticket_no = f"HT-{session.code}-{student.register_number}"
                ht, created = HallTicket.objects.get_or_create(
                    session=session,
                    student=student,
                    defaults={
                        'ticket_number': ticket_no,
                        'is_eligible': True,
                        'eligibility_remarks': 'Cleared academic & fee requirements'
                    }
                )
                if created:
                    created_count += 1

        return Response({
            'success': True,
            'message': f"Generated {created_count} new hall tickets for session {session.code}.",
            'total_hall_tickets': HallTicket.objects.filter(session=session).count()
        })

    @action(detail=True, methods=['get'], url_path='download-pdf')
    def download_pdf(self, request, pk=None):
        """
        Downloads a locally generated PDF Hall Ticket.
        """
        hall_ticket = self.get_object()
        hall_ticket.download_count += 1
        hall_ticket.last_downloaded_at = timezone.now()
        hall_ticket.save()

        pdf_bytes = generate_hall_ticket_pdf(hall_ticket)
        filename = f"HallTicket_{hall_ticket.student.register_number}_{hall_ticket.session.code}.pdf"
        
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
