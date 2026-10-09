"""
ExamForge M2 — Academic Service Layer
=======================================
Business logic for academic entity management.
"""

import logging
from typing import Dict, Any, List
from django.db.models import Count, Q

from academics.models import (
    Department, Course, Branch, Semester, AcademicYear, Subject, StatusChoices
)

logger = logging.getLogger(__name__)


class AcademicService:
    """Encapsulates academic management business logic."""

    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """Compute real dashboard statistics for academic management."""
        departments = Department.objects.all()
        courses = Course.objects.all()
        branches = Branch.objects.all()
        semesters = Semester.objects.all()
        subjects = Subject.objects.all()
        academic_years = AcademicYear.objects.all()

        # Subjects by type
        from django.db.models import Count
        subjects_by_type_qs = subjects.values('subject_type').annotate(count=Count('id'))
        subjects_by_type = {item['subject_type']: item['count'] for item in subjects_by_type_qs}

        # Departments summary
        dept_summary = list(
            departments.filter(status=StatusChoices.ACTIVE).annotate(
                course_count=Count('courses', filter=Q(courses__status='active')),
                student_count=Count('students', filter=Q(students__status='active')),
                subject_count=Count('subjects', filter=Q(subjects__status='active')),
            ).values('id', 'code', 'name', 'course_count', 'student_count', 'subject_count')
            .order_by('name')
        )

        return {
            'total_departments': departments.count(),
            'active_departments': departments.filter(status=StatusChoices.ACTIVE).count(),
            'total_courses': courses.count(),
            'active_courses': courses.filter(status=StatusChoices.ACTIVE).count(),
            'total_branches': branches.count(),
            'total_semesters': semesters.count(),
            'total_subjects': subjects.count(),
            'active_subjects': subjects.filter(status=StatusChoices.ACTIVE).count(),
            'total_academic_years': academic_years.count(),
            'current_academic_year': AcademicYear.get_current(),
            'subjects_by_type': subjects_by_type,
            'departments_summary': dept_summary,
        }

    @staticmethod
    def get_academic_tree() -> List[Dict]:
        """
        Return a nested tree of the entire academic structure:
        Department → Courses → Branches → Semesters → Subjects
        """
        tree = []
        departments = Department.objects.filter(
            status=StatusChoices.ACTIVE
        ).prefetch_related(
            'courses__branches',
            'courses__semesters__subjects',
        ).order_by('code')

        for dept in departments:
            dept_node = {
                'id': dept.id,
                'code': dept.code,
                'name': dept.name,
                'courses': [],
            }
            for course in dept.courses.filter(status=StatusChoices.ACTIVE).order_by('code'):
                course_node = {
                    'id': course.id,
                    'code': course.code,
                    'name': course.name,
                    'duration_years': course.duration_years,
                    'total_semesters': course.total_semesters,
                    'branches': [],
                    'semesters': [],
                }
                for branch in course.branches.filter(status=StatusChoices.ACTIVE).order_by('code'):
                    course_node['branches'].append({
                        'id': branch.id,
                        'code': branch.code,
                        'name': branch.name,
                    })
                for sem in course.semesters.filter(status=StatusChoices.ACTIVE).order_by('semester_number'):
                    sem_node = {
                        'id': sem.id,
                        'number': sem.semester_number,
                        'name': sem.name,
                        'subjects': [],
                    }
                    for subject in sem.subjects.filter(status=StatusChoices.ACTIVE).order_by('code'):
                        sem_node['subjects'].append({
                            'id': subject.id,
                            'code': subject.code,
                            'name': subject.name,
                            'type': subject.subject_type,
                            'credits': subject.credits,
                        })
                    course_node['semesters'].append(sem_node)
                dept_node['courses'].append(course_node)
            tree.append(dept_node)
        return tree

    @staticmethod
    def get_eligible_subjects_for_student(student) -> List[Dict]:
        """Return subjects available to a specific student based on their program."""
        from students.models import Student
        subjects = Subject.objects.filter(
            course=student.course,
            semester=student.current_semester,
            status=StatusChoices.ACTIVE,
        ).filter(
            Q(branch=student.branch) | Q(branch__isnull=True)
        ).select_related('semester', 'department').order_by('code')

        return list(subjects.values(
            'id', 'code', 'name', 'subject_type', 'credits',
            'is_external_exam', 'is_internal_exam',
            'max_external_marks', 'max_internal_marks',
        ))
