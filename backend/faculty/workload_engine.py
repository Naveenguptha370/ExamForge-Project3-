"""
ExamForge - Faculty Invigilation Workload Balancer
Member 1: Faculty Management
"""
from typing import Dict, Any, List
import statistics
from faculty.models import FacultyProfile

class FacultyWorkloadCalculator:
    """
    Computes cumulative invigilation duties, calculates seniority-adjusted equity ratings,
    and identifies under-allocated and overburdened faculty members.
    """
    DESIGNATION_TARGETS = {
        'Professor': 3,
        'Associate Professor': 5,
        'Assistant Professor': 8
    }

    @classmethod
    def get_target_duties(cls, designation: str) -> int:
        return cls.DESIGNATION_TARGETS.get(designation, 6)

    @classmethod
    def calculate_workload_metrics(cls, department: str = None) -> Dict[str, Any]:
        profiles = FacultyProfile.objects.filter(status='ACTIVE')
        if department:
            profiles = profiles.filter(department=department)

        workload_data = []
        assigned_counts = []

        for p in profiles:
            target = cls.get_target_duties(p.designation)
            # In a full system, count assigned duties from invigilation duties
            current_assigned = getattr(p, 'completed_duties_count', 0)
            assigned_counts.append(current_assigned)
            delta = current_assigned - target
            equity_status = "BALANCED"
            if delta < -2:
                equity_status = "UNDER_ALLOCATED"
            elif delta > 2:
                equity_status = "OVERBURDENED"

            workload_data.append({
                'faculty_id': p.faculty_id,
                'name': p.user.get_full_name() or p.user.username,
                'department': p.department,
                'designation': p.designation,
                'target_duties': target,
                'current_assigned': current_assigned,
                'equity_status': equity_status
            })

        mean_val = statistics.mean(assigned_counts) if assigned_counts else 0.0
        stdev_val = statistics.stdev(assigned_counts) if len(assigned_counts) > 1 else 0.0

        return {
            'total_faculty_evaluated': len(workload_data),
            'department_filter': department or 'ALL',
            'average_duties': round(mean_val, 2),
            'variance_standard_deviation': round(stdev_val, 2),
            'faculty_workloads': workload_data
        }
