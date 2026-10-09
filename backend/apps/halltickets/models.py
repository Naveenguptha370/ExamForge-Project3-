import uuid
from django.db import models
from apps.students.models import StudentProfile
from apps.examinations.models import ExamSession, ExamSubject

class HallTicket(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='hall_tickets')
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='hall_tickets')
    ticket_number = models.CharField(max_length=60, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    verification_hash = models.CharField(max_length=64, default=uuid.uuid4)
    is_blocked = models.BooleanField(default=False)
    block_reason = models.TextField(blank=True, default='')
    download_count = models.IntegerField(default=0)
    pdf_file = models.FileField(upload_to='hall_tickets/', null=True, blank=True)

    class Meta:
        unique_together = ('student', 'exam_session')
        ordering = ['student__roll_no']

    def __str__(self):
        return f"{self.ticket_number} - {self.student.roll_no} ({self.exam_session.session_code})"


class HallTicketEntry(models.Model):
    hall_ticket = models.ForeignKey(HallTicket, on_delete=models.CASCADE, related_name='entries')
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    exam_date = models.DateField()
    time_slot_str = models.CharField(max_length=100)
    room_number = models.CharField(max_length=30)
    seat_label = models.CharField(max_length=20)

    class Meta:
        ordering = ['exam_date', 'time_slot_str']

    def __str__(self):
        return f"{self.hall_ticket.ticket_number}: {self.exam_subject.subject.code} in {self.room_number} ({self.seat_label})"
