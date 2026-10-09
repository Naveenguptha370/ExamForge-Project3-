"""
ExamForge - Department Faculty Directory Manager
Member 1: Faculty Management
"""
from typing import Dict, Any, List
from faculty.models import FacultyProfile

class DepartmentDirectoryManager:
    @classmethod
    def get_department_roster(cls, department: str) -> List[Dict[str, Any]]:
        profiles = FacultyProfile.objects.filter(department=department).order_by('designation')
        return [
            {
                'id': p.id,
                'faculty_id': p.faculty_id,
                'designation': p.designation,
                'status': p.status,
                'email': p.email
            }
            for p in profiles
        ]
