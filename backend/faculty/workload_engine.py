"""
ExamForge - Faculty Invigilation Workload Balancer
Member 1: Faculty Management
"""
from typing import Dict, Any, List
from faculty.models import FacultyProfile

class FacultyWorkloadCalculator:
    DESIGNATION_TARGETS = {'Professor': 3, 'Associate Professor': 5, 'Assistant Professor': 8}

    @classmethod
    def get_target_duties(cls, designation: str) -> int:
        return cls.DESIGNATION_TARGETS.get(designation, 6)

    @classmethod
    def calculate_workload_metrics(cls, department: str = None) -> Dict[str, Any]:
        profiles = FacultyProfile.objects.filter(status='ACTIVE')
        if department:
            profiles = profiles.filter(department=department)
        return {
            'total_evaluated': profiles.count(),
            'average_target': 5.5
        }
