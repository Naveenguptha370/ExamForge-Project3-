"""
ExamForge - Faculty Availability Matrix & Conflict Solver
Member 1: Faculty Management
"""
from typing import Dict, Any, List, Tuple
from datetime import time
from faculty.models import FacultyAvailability

class AvailabilitySlotSolver:
    DAYS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']

    @classmethod
    def validate_slot_times(cls, start_time: time, end_time: time) -> Tuple[bool, str]:
        if start_time >= end_time:
            return (False, "Start time must precede end time.")
        duration = (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute)
        if duration < 30:
            return (False, "Slot duration must be at least 30 minutes.")
        return (True, "")

    @classmethod
    def check_overlap(cls, faculty_id: int, day_of_week: str, start_time: time, end_time: time) -> bool:
        slots = FacultyAvailability.objects.filter(faculty_id=faculty_id, day_of_week=day_of_week)
        for s in slots:
            if max(start_time, s.start_time) < min(end_time, s.end_time):
                return True
        return False
