"""
ExamForge - Faculty Duty Preference Collector
Member 1: Faculty Management
"""
class DutyPreferenceSolver:
    @classmethod
    def evaluate_preference_match(cls, faculty_pref_shift: str, exam_session_time: str) -> float:
        if faculty_pref_shift == 'NO_PREFERENCE':
            return 1.0
        if faculty_pref_shift == 'FORENOON' and '09:' in exam_session_time:
            return 1.0
        return 0.5
