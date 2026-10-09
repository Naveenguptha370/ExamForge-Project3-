from django.db import models

class Department(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    head_of_department = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    duration_years = models.IntegerField(default=4)
    degree_type = models.CharField(max_length=50, default='Undergraduate')

    def __str__(self):
        return f"{self.code} ({self.name})"


class Branch(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='branches')

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Semester(models.Model):
    class Term(models.TextChoices):
        ODD = 'ODD', 'Odd Semester'
        EVEN = 'EVEN', 'Even Semester'

    number = models.IntegerField(help_text='Semester number (1-8)')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    term = models.CharField(max_length=10, choices=Term.choices, default=Term.ODD)
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ('number', 'academic_year', 'term')
        ordering = ['academic_year', 'number']

    def __str__(self):
        return f"Sem {self.number} ({self.academic_year} {self.term})"


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    credits = models.DecimalField(max_digits=4, decimal_places=1, default=3.0)
    is_elective = models.BooleanField(default=False)
    min_attendance_pct = models.IntegerField(default=75)
    syllabus_summary = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code}: {self.name}"
