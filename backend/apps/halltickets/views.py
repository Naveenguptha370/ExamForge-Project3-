import os
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django.db import transaction
from django.core.files.base import ContentFile
from .models import HallTicket, HallTicketEntry
from .serializers import HallTicketSerializer
from .pdf_generator import generate_hall_ticket_pdf
from apps.students.models import StudentProfile
from apps.examinations.models import ExamSession, ExamSubject
from apps.registration.models import SubjectRegistration
from apps.seating.models import SeatAllocation
from apps.scheduling.models import TimetableEntry

class HallTicketViewSet(viewsets.ModelViewSet):
    queryset = HallTicket.objects.select_related('student__department', 'student__course', 'exam_session').prefetch_related('entries__exam_subject__subject').all()
    serializer_class = HallTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        student_id = self.request.query_params.get('student')
        session_id = self.request.query_params.get('exam_session')
        roll_no = self.request.query_params.get('roll_no')

        # If student role, restrict to their own hall tickets
        if hasattr(self.request.user, 'student_profile'):
            return qs.filter(student=self.request.user.student_profile)

        if student_id:
            qs = qs.filter(student_id=student_id)
        if session_id:
            qs = qs.filter(exam_session_id=session_id)
        if roll_no:
            qs = qs.filter(student__roll_no__iexact=roll_no)
        return qs

    @action(detail=False, methods=['post'])
    def generate_individual(self, request):
        student_id = request.data.get('student_id')
        session_id = request.data.get('exam_session_id')

        if not student_id or not session_id:
            return Response({'error': 'student_id and exam_session_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        student = StudentProfile.objects.filter(id=student_id).first()
        session = ExamSession.objects.filter(id=session_id).first()

        if not student or not session:
            return Response({'error': 'Student or Exam Session not found'}, status=status.HTTP_404_NOT_FOUND)

        if not student.is_eligible_for_exam:
            return Response({'error': f'Student {student.roll_no} is marked ineligible for examinations.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check subject registrations for attendance shortage / dues
        registrations = SubjectRegistration.objects.filter(student=student, is_approved=True)
        ineligible_regs = registrations.exclude(eligibility_status='ELIGIBLE')
        if ineligible_regs.exists():
            reasons = [f"{r.subject.code}: {r.get_eligibility_status_display()}" for r in ineligible_regs]
            return Response({'error': f'Cannot issue hall ticket due to eligibility issues: {", ".join(reasons)}'}, status=status.HTTP_400_BAD_REQUEST)

        ticket_number = f"HT-{session.session_code}-{student.roll_no}"

        with transaction.atomic():
            ticket, created = HallTicket.objects.get_or_create(
                student=student,
                exam_session=session,
                defaults={'ticket_number': ticket_number}
            )
            ticket.entries.all().delete()

            # Find all exam subjects enrolled by this student
            enrolled_subject_ids = registrations.values_list('subject_id', flat=True)
            exam_subjects = ExamSubject.objects.filter(exam_session=session, subject_id__in=enrolled_subject_ids)

            for es in exam_subjects:
                # Find date & slot from timetable or exam subject
                exam_date = es.planned_date
                time_slot_str = f"{es.time_slot.name} ({es.time_slot.start_time.strftime('%I:%M %p')} - {es.time_slot.end_time.strftime('%I:%M %p')})" if es.time_slot else "TBD"

                # Find allocated room and seat from SeatAllocation
                allocation = SeatAllocation.objects.filter(seating_plan__exam_subject=es, student=student).select_related('seating_plan__room', 'seat').first()

                room_no = allocation.seating_plan.room.room_number if allocation else "Hall TBD"
                seat_label = allocation.seat.seat_label if allocation else "Seat TBD"

                if exam_date:
                    HallTicketEntry.objects.create(
                        hall_ticket=ticket,
                        exam_subject=es,
                        exam_date=exam_date,
                        time_slot_str=time_slot_str,
                        room_number=room_no,
                        seat_label=seat_label
                    )

            # Generate PDF
            pdf_bytes = generate_hall_ticket_pdf(ticket)
            ticket.pdf_file.save(f"{ticket.ticket_number}.pdf", ContentFile(pdf_bytes), save=True)

        return Response({
            'message': f'Hall ticket generated successfully for {student.roll_no}',
            'hall_ticket': HallTicketSerializer(ticket).data
        })

    @action(detail=False, methods=['post'])
    def bulk_generate(self, request):
        session_id = request.data.get('exam_session_id')
        dept_id = request.data.get('department_id')

        if not session_id:
            return Response({'error': 'exam_session_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        session = ExamSession.objects.filter(id=session_id).first()
        if not session:
            return Response({'error': 'Exam session not found'}, status=status.HTTP_404_NOT_FOUND)

        students_qs = StudentProfile.objects.filter(status='ACTIVE', is_eligible_for_exam=True)
        if dept_id:
            students_qs = students_qs.filter(department_id=dept_id)

        students = list(students_qs)
        generated_count = 0
        skipped_count = 0

        for st in students:
            # Check eligibility
            ineligible = SubjectRegistration.objects.filter(student=st, is_approved=True).exclude(eligibility_status='ELIGIBLE').exists()
            if ineligible:
                skipped_count += 1
                continue

            ticket_number = f"HT-{session.session_code}-{st.roll_no}"
            ticket, _ = HallTicket.objects.get_or_create(
                student=st,
                exam_session=session,
                defaults={'ticket_number': ticket_number}
            )
            ticket.entries.all().delete()

            # Enrolled subjects
            subject_ids = SubjectRegistration.objects.filter(student=st, is_approved=True, eligibility_status='ELIGIBLE').values_list('subject_id', flat=True)
            exam_subjects = ExamSubject.objects.filter(exam_session=session, subject_id__in=subject_ids)

            for es in exam_subjects:
                if es.planned_date:
                    alloc = SeatAllocation.objects.filter(seating_plan__exam_subject=es, student=st).select_related('seating_plan__room', 'seat').first()
                    room_no = alloc.seating_plan.room.room_number if alloc else "Hall TBD"
                    seat_label = alloc.seat.seat_label if alloc else "Seat TBD"
                    slot_str = f"{es.time_slot.name} ({es.time_slot.start_time.strftime('%I:%M %p')})" if es.time_slot else "TBD"

                    HallTicketEntry.objects.create(
                        hall_ticket=ticket,
                        exam_subject=es,
                        exam_date=es.planned_date,
                        time_slot_str=slot_str,
                        room_number=room_no,
                        seat_label=seat_label
                    )

            pdf_bytes = generate_hall_ticket_pdf(ticket)
            ticket.pdf_file.save(f"{ticket.ticket_number}.pdf", ContentFile(pdf_bytes), save=True)
            generated_count += 1

        return Response({
            'message': f'Bulk Hall Ticket Generation Complete: {generated_count} issued, {skipped_count} skipped due to ineligibility.',
            'generated_count': generated_count,
            'skipped_count': skipped_count
        })

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        ticket = self.get_object()
        if ticket.is_blocked:
            return Response({'error': f'Hall ticket blocked: {ticket.block_reason}'}, status=status.HTTP_403_FORBIDDEN)

        pdf_bytes = generate_hall_ticket_pdf(ticket)
        ticket.download_count += 1
        ticket.save()

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{ticket.ticket_number}.pdf"'
        return response

    @action(detail=True, methods=['get'])
    def preview_pdf(self, request, pk=None):
        ticket = self.get_object()
        pdf_bytes = generate_hall_ticket_pdf(ticket)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{ticket.ticket_number}.pdf"'
        return response

    @action(detail=True, methods=['post'])
    def toggle_block(self, request, pk=None):
        ticket = self.get_object()
        reason = request.data.get('reason', 'Administrative block')
        ticket.is_blocked = not ticket.is_blocked
        ticket.block_reason = reason if ticket.is_blocked else ''
        ticket.save()
        status_str = 'BLOCKED' if ticket.is_blocked else 'UNBLOCKED'
        return Response({'message': f'Hall ticket {ticket.ticket_number} is now {status_str}.', 'is_blocked': ticket.is_blocked})
