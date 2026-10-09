"""
ExamForge - Faculty Duty Preference Collector
Member 1: Faculty Management
"""
from typing import Dict, Any, List
from datetime import date

class DutyPreferenceSolver:
    """
    Captures faculty preferences for exam shifts (Forenoon vs Afternoon)
    and evaluates proximity to specific academic blocks.
    """
    SHIFTS = ['FORENOON', 'AFTERNOON', 'NO_PREFERENCE']

    @classmethod
    def evaluate_preference_match(
        cls,
        faculty_pref_shift: str,
        exam_session_time: str
    ) -> float:
        if faculty_pref_shift == 'NO_PREFERENCE':
            return 1.0
        if faculty_pref_shift == 'FORENOON' and '09:' in exam_session_time:
            return 1.0
        if faculty_pref_shift == 'AFTERNOON' and ('13:' in exam_session_time or '14:' in exam_session_time):
            return 1.0
        return 0.5
