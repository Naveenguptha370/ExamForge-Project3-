from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from apps.accounts.models import User, UserRole
from apps.students.models import Student, SubjectRegistration, EligibilityStatus
from apps.faculty.models import FacultyProfile, FacultyStatus
from apps.infrastructure.models import Room
from apps.academics.models import Department, Subject, Branch
from apps.examinations.models import ExamSession, SessionStatus, ExamSubjectConfig
from apps.scheduling.models import Timetable, TimetableEntry, SchedulingClash
from apps.seating.models import SeatingPlan, RoomAllocation
from apps.invigilation.models import InvigilatorDuty
from apps.halltickets.models import HallTicket
from apps.attendance.models import AttendanceRecord

class DashboardOverviewView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_students = Student.objects.count()
        active_students = Student.objects.filter(status='ACTIVE').count()
        total_faculty = FacultyProfile.objects.count()
        available_faculty = FacultyProfile.objects.filter(status=FacultyStatus.ACTIVE, is_eligible_for_invigilation=True).count()
        total_rooms = Room.objects.filter(is_active=True).count()
        total_capacity = sum(Room.objects.filter(is_active=True).values_list('usable_exam_capacity', flat=True)) or 0
        total_departments = Department.objects.filter(is_active=True).count()
        total_subjects = Subject.objects.filter(is_active=True).count()

        # Active or Latest Exam Session
        latest_session = ExamSession.objects.order_by('-start_date').first()
        session_data = None
        readiness_score = 0
        readiness_breakdown = {
            'subjects_configured': 0,
            'timetable_validated': 0,
            'seating_arranged': 0,
            'invigilators_assigned': 0,
            'hall_tickets_generated': 0
        }

        if latest_session:
            total_cfg = latest_session.configured_subjects.count()
            has_tt = hasattr(latest_session, 'timetable') and latest_session.timetable is not None
            tt_valid = has_tt and latest_session.timetable.is_conflict_free
            
            plans_count = latest_session.seating_plans.count()
            duties_count = latest_session.invigilator_duties.count()
            tickets_count = latest_session.hall_tickets.count()

            # Calculate weighted readiness score
            # 20% subjects + 30% timetable + 20% seating + 15% invigilators + 15% hall tickets
            score = 0
            if total_cfg > 0:
                score += 20
                readiness_breakdown['subjects_configured'] = 100
            if tt_valid:
                score += 30
                readiness_breakdown['timetable_validated'] = 100
            elif has_tt:
                score += 15
                readiness_breakdown['timetable_validated'] = 50
            
            if plans_count > 0:
                score += 20
                readiness_breakdown['seating_arranged'] = 100
            if duties_count > 0:
                score += 15
                readiness_breakdown['invigilators_assigned'] = 100
            if tickets_count > 0:
                score += 15
                readiness_breakdown['hall_tickets_generated'] = 100

            readiness_score = score

            session_data = {
                'id': latest_session.id,
                'name': latest_session.name,
                'code': latest_session.code,
                'academic_year': latest_session.academic_year,
                'status': latest_session.status,
                'status_display': latest_session.get_status_display(),
                'start_date': str(latest_session.start_date),
                'end_date': str(latest_session.end_date),
                'total_configured_subjects': total_cfg,
                'has_timetable': has_tt,
                'timetable_status': latest_session.timetable.get_status_display() if has_tt else 'Not Generated',
                'timetable_conflict_free': latest_session.timetable.is_conflict_free if has_tt else False,
                'timetable_clash_count': latest_session.timetable.clash_count if has_tt else 0,
                'total_exams_scheduled': latest_session.timetable.total_exams_scheduled if has_tt else 0,
                'total_slots_used': latest_session.timetable.total_slots_used if has_tt else 0,
                'total_seating_plans': plans_count,
                'total_invigilator_duties': duties_count,
                'total_hall_tickets': tickets_count,
            }

        # Daily Exam Load breakdown
        daily_load = []
        if latest_session and hasattr(latest_session, 'timetable'):
            daily_stats = latest_session.timetable.entries.values('exam_date').annotate(
                exam_count=Count('id'),
                student_sum=Sum('expected_students')
            ).order_by('exam_date')
            for d in daily_stats:
                daily_load.append({
                    'date': str(d['exam_date']),
                    'day': d['exam_date'].strftime('%a'),
                    'exam_count': d['exam_count'],
                    'students': d['student_sum'] or 0
                })

        # Department-wise breakdown
        dept_stats = []
        for dept in Department.objects.filter(is_active=True):
            dept_stats.append({
                'code': dept.code,
                'name': dept.name,
                'courses': dept.courses.count(),
                'subjects': dept.subjects.count(),
                'faculty': dept.faculty_members.count()
            })

        return Response({
            'success': True,
            'summary': {
                'total_students': total_students,
                'active_students': active_students,
                'total_faculty': total_faculty,
                'available_faculty': available_faculty,
                'total_rooms': total_rooms,
                'total_capacity': total_capacity,
                'total_departments': total_departments,
                'total_subjects': total_subjects,
                'readiness_score': readiness_score,
                'readiness_breakdown': readiness_breakdown
            },
            'active_session': session_data,
            'daily_load': daily_load,
            'departments': dept_stats
        })
