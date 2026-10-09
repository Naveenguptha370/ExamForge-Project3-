import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.examinations.models import ExamSession
from apps.students.models import Student

class HallTicket(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='hall_tickets')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='hall_tickets')
    ticket_number = models.CharField(max_length=64, unique=True, db_index=True)
    barcode_token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_eligible = models.BooleanField(default=True)
    eligibility_remarks = models.CharField(max_length=255, blank=True, default='Cleared all academic & attendance requirements.')
    download_count = models.PositiveIntegerField(default=0)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'student')
        ordering = ['student__register_number']
        verbose_name = _('Hall Ticket')
        verbose_name_plural = _('Hall Tickets')

    def __str__(self):
        return f"HT: {self.ticket_number} - {self.student.register_number} ({self.student.full_name})"
