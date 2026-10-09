from django.db import models
from django.utils.translation import gettext_lazy as _

class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    head_of_department = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return f"{self.code} - {self.name}"


class DegreeType(models.TextChoices):
    BTECH = 'B.Tech', _('Bachelor of Technology')
    MTECH = 'M.Tech', _('Master of Technology')
    BCA = 'BCA', _('Bachelor of Computer Applications')
    MCA = 'MCA', _('Master of Computer Applications')
    BSC = 'B.Sc', _('Bachelor of Science')
    MSC = 'M.Sc', _('Master of Science')
    BBA = 'BBA', _('Bachelor of Business Administration')
    MBA = 'MBA', _('Master of Business Administration')


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    degree_type = models.CharField(max_length=20, choices=DegreeType.choices, default=DegreeType.BTECH)
    duration_years = models.PositiveIntegerField(default=4)
    total_semesters = models.PositiveIntegerField(default=8)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        return f"{self.code} - {self.name} ({self.degree_type})"


class Branch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='branches')
    code = models.CharField(max_length=20, db_index=True)
    name = models.CharField(max_length=150)
    intake_capacity = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('course', 'code')
        ordering = ['code']
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')

    def __str__(self):
        return f"{self.course.code} / {self.code} - {self.name}"


class Semester(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=20, default='2025-2026')
    term = models.CharField(max_length=10, choices=[('ODD', 'Odd Term'), ('EVEN', 'Even Term')], default='ODD')
    is_current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('branch', 'semester_number', 'academic_year')
        ordering = ['semester_number']
        verbose_name = _('Semester')
        verbose_name_plural = _('Semesters')

    def __str__(self):
        return f"{self.branch.name} - Sem {self.semester_number} ({self.academic_year})"


class SubjectType(models.TextChoices):
    THEORY = 'THEORY', _('Theory')
    PRACTICAL = 'PRACTICAL', _('Practical / Lab')
    INTEGRATED = 'INTEGRATED', _('Integrated (Theory + Lab)')
    PROJECT = 'PROJECT', _('Project / Seminar')


class DifficultyLevel(models.TextChoices):
    EASY = 'EASY', _('Easy')
    MEDIUM = 'MEDIUM', _('Medium')
    HARD = 'HARD', _('Hard / Heavy Computation')


class Subject(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    semester_number = models.PositiveIntegerField(default=1)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    subject_type = models.CharField(max_length=20, choices=SubjectType.choices, default=SubjectType.THEORY)
    credits = models.DecimalField(max_digits=3, decimal_places=1, default=3.0)
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    difficulty = models.CharField(max_length=20, choices=DifficultyLevel.choices, default=DifficultyLevel.MEDIUM)
    is_elective = models.BooleanField(default=False)
    requires_special_lab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return f"[{self.code}] {self.name} (Sem {self.semester_number})"
