"""
ExamForge - Faculty Availability Matrix & Conflict Solver
Member 1: Faculty Management
"""
from typing import Dict, Any, List, Tuple
from datetime import time
from faculty.models import FacultyAvailability, FacultyProfile

class AvailabilitySlotSolver:
    """
    Validates, manages, and resolves faculty availability across weekly examination slots.
    Ensures zero overlapping intervals and validates adherence to examination session timings.
    """
    DAYS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

    @classmethod
    def validate_slot_times(cls, start_time: time, end_time: time) -> Tuple[bool, str]:
        if start_time >= end_time:
            return (False, "Start time must precede end time.")
        duration_minutes = (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute)
        if duration_minutes < 30:
            return (False, "Slot duration must be at least 30 minutes.")
        return (True, "")

    @classmethod
    def check_overlap(
        cls,
        faculty_id: int,
        day_of_week: str,
        start_time: time,
        end_time: time,
        exclude_id: int = None
    ) -> bool:
        slots = FacultyAvailability.objects.filter(faculty_id=faculty_id, day_of_week=day_of_week)
        if exclude_id:
            slots = slots.exclude(id=exclude_id)

        for s in slots:
            # Overlap condition: start < other_end and end > other_start
            if max(start_time, s.start_time) < min(end_time, s.end_time):
                return True
        return False

    @classmethod
    def get_weekly_matrix(cls, faculty_id: int) -> Dict[str, List[Dict[str, Any]]]:
        matrix = {day: [] for day in cls.DAYS}
        slots = FacultyAvailability.objects.filter(faculty_id=faculty_id).order_by('start_time')
        for s in slots:
            matrix[s.day_of_week].append({
                'id': s.id,
                'start_time': s.start_time.strftime('%H:%M'),
                'end_time': s.end_time.strftime('%H:%M'),
                'is_available': s.is_available
            })
        return matrix
