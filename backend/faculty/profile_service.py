"""
ExamForge - Extended Faculty Profile & Accreditation Service
Member 1: Faculty Management
"""
from typing import Dict, Any, Optional
from datetime import date
from faculty.models import FacultyProfile

class FacultyAccreditationService:
    @classmethod
    def calculate_experience_years(cls, date_of_joining: Optional[date]) -> float:
        if not date_of_joining:
            return 0.0
        today = date.today()
        days = (today - date_of_joining).days
        return round(max(0.0, days / 365.25), 1)

    @classmethod
    def evaluate_invigilation_eligibility(cls, profile: FacultyProfile) -> Dict[str, Any]:
        is_eligible = profile.status == 'ACTIVE' and bool(profile.email)
        return {
            'faculty_id': profile.faculty_id,
            'is_eligible': is_eligible,
            'duty_tier': "CHIEF_INVIGILATOR" if 'Professor' in profile.designation else "ROOM_INVIGILATOR",
            'experience_years': cls.calculate_experience_years(profile.date_of_joining)
        }
