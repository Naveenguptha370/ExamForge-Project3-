from django.db import models

class SystemSetting(models.Model):
    institution_name = models.CharField(max_length=200, default='ExamForge University')
    institution_code = models.CharField(max_length=30, default='EFU-TECH')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    current_term = models.CharField(max_length=10, default='EVEN')
    contact_email = models.EmailField(default='coe@examforge.edu')
    contact_phone = models.CharField(max_length=20, default='+91 98765 43210')
    address = models.TextField(default='Knowledge Park, Higher Education Complex, Hyderabad, India')
    min_attendance_threshold = models.IntegerField(default=75)
    default_exam_duration_mins = models.IntegerField(default=180)
    default_spacing_rule = models.CharField(max_length=50, default='ALTERNATE_COLS')
    hall_ticket_instructions = models.TextField(
        default='1. Carry this Hall Ticket and ID card.\n2. Arrive 20 mins early.\n3. Electronic gadgets strictly prohibited.\n4. Comply with all invigilator instructions.'
    )
    malpractice_policy = models.TextField(
        default='Any malpractice or possession of unapproved notes will lead to debarment from the examination and disciplinary hearing.'
    )
    enable_audit_logging = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.institution_name} Settings ({self.academic_year})"
