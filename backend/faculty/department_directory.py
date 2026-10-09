"""
ExamForge - Department Faculty Directory Manager
Member 1: Faculty Management
"""
from typing import Dict, Any, List
from django.db.models import Count, Q
from faculty.models import FacultyProfile

class DepartmentDirectoryManager:
    """Manages departmental faculty structures, rosters, and supervisory hierarchies."""

    @classmethod
    def list_departments(cls) -> List[Dict[str, Any]]:
        queryset = FacultyProfile.objects.values('department').annotate(
            total_count=Count('id'),
            active_count=Count('id', filter=Q(status='ACTIVE')),
            leave_count=Count('id', filter=Q(status='ON_LEAVE'))
        ).order_by('department')
        return list(queryset)

    @classmethod
    def get_department_roster(cls, department: str) -> List[Dict[str, Any]]:
        profiles = FacultyProfile.objects.filter(department=department).order_by('designation', 'faculty_id')
        roster = []
        for p in profiles:
            roster.append({
                'id': p.id,
                'faculty_id': p.faculty_id,
                'name': p.user.get_full_name() or p.user.username,
                'designation': p.designation,
                'status': p.status,
                'email': p.email,
                'phone': p.phone,
                'specialization': p.specialization
            })
        return roster

    @classmethod
    def search_faculty(cls, query: str) -> List[Dict[str, Any]]:
        q = query.strip()
        matches = FacultyProfile.objects.filter(
            Q(faculty_id__icontains=q) |
            Q(department__icontains=q) |
            Q(designation__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(specialization__icontains=q)
        ).distinct()[:50]
        return [
            {
                'id': m.id,
                'faculty_id': m.faculty_id,
                'name': m.user.get_full_name() or m.user.username,
                'department': m.department,
                'designation': m.designation,
                'status': m.status
            }
            for m in matches
        ]
