"""
ExamForge - Extended Faculty Profile & Accreditation Service
Member 1: Faculty Management
"""
from typing import Dict, Any, List, Optional
from datetime import date
from faculty.models import FacultyProfile

class FacultyAccreditationService:
    """
    Evaluates faculty qualification levels, institutional seniority, and invigilation eligibility.
    Aligns with university statutory guidelines and accreditation bodies (AICTE/UGC/NIRF).
    """
    SENIOR_DESIGNATIONS = {'Professor', 'Associate Professor', 'Dean', 'Head of Department'}
    ELIGIBLE_INVIGILATOR_STATUSES = {'ACTIVE'}

    @classmethod
    def calculate_experience_years(cls, date_of_joining: Optional[date]) -> float:
        if not date_of_joining:
            return 0.0
        today = date.today()
        days = (today - date_of_joining).days
        return round(max(0.0, days / 365.25), 1)

    @classmethod
    def evaluate_invigilation_eligibility(cls, profile: FacultyProfile) -> Dict[str, Any]:
        reasons = []
        is_eligible = True

        if profile.status not in cls.ELIGIBLE_INVIGILATOR_STATUSES:
            is_eligible = False
            reasons.append(f"Faculty status is '{profile.status}' (Must be ACTIVE)")

        if not profile.email or '@' not in profile.email:
            is_eligible = False
            reasons.append("Valid institutional email address is missing")

        if not profile.phone or len(profile.phone) < 10:
            is_eligible = False
            reasons.append("Registered emergency contact telephone number is missing or incomplete")

        is_senior = profile.designation in cls.SENIOR_DESIGNATIONS
        duty_tier = "CHIEF_INVIGILATOR" if is_senior else "ROOM_INVIGILATOR"

        return {
            'faculty_id': profile.faculty_id,
            'is_eligible': is_eligible,
            'duty_tier': duty_tier,
            'experience_years': cls.calculate_experience_years(profile.date_of_joining),
            'disqualification_reasons': reasons
        }

    @classmethod
    def get_department_faculty_summary(cls, department: str) -> Dict[str, Any]:
        profiles = FacultyProfile.objects.filter(department=department)
        total = profiles.count()
        active = profiles.filter(status='ACTIVE').count()
        on_leave = profiles.filter(status='ON_LEAVE').count()
        phd_holders = profiles.filter(qualification__icontains='Ph.D').count()

        return {
            'department': department,
            'total_faculty': total,
            'active_faculty': active,
            'on_leave': on_leave,
            'phd_qualified': phd_holders,
            'readiness_percentage': round((active / total * 100) if total > 0 else 0, 1)
        }
