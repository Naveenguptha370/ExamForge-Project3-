from django.db import models
from django.conf import settings

class GeneratedReport(models.Model):
    class ReportType(models.TextChoices):
        EXECUTIVE_SUMMARY = 'EXECUTIVE_SUMMARY', 'Executive Examination Summary'
        READINESS_INDEX = 'READINESS_INDEX', 'Examination Readiness Index'
        ROOM_UTILIZATION = 'ROOM_UTILIZATION', 'Room & Infrastructure Utilization'
        SEATING_COMPLETION = 'SEATING_COMPLETION', 'Seating Arrangement Report'
        INVIGILATION_WORKLOAD = 'INVIGILATION_WORKLOAD', 'Invigilator Workload Distribution'
        ATTENDANCE_SUMMARY = 'ATTENDANCE_SUMMARY', 'Examination Attendance & Malpractice Report'

    report_type = models.CharField(max_length=40, choices=ReportType.choices)
    title = models.CharField(max_length=200)
    parameters = models.JSONField(default=dict, blank=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    file_format = models.CharField(max_length=10, default='PDF')
    file_path = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
