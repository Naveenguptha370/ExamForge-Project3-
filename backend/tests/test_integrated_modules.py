import io
import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.accounts.models import UserRole, UserActivity
from apps.academics.models import Department, Course, Branch, Semester, Subject
from apps.students.models import Student, SubjectRegistration, EligibilityStatus
from apps.faculty.models import FacultyProfile, Designation, FacultyStatus
from apps.infrastructure.models import Block, Room, RoomType
from apps.examinations.models import ExamSession, TimeSlot, ExamSubjectConfig
from apps.scheduling.models import Timetable, TimetableEntry
from apps.seating.models import SeatingPlan, RoomAllocation, SeatAssignment
from apps.invigilation.models import InvigilatorDuty, DutyRole, DutyStatus
from apps.halltickets.models import HallTicket
from apps.halltickets.pdf_generator import generate_hall_ticket_pdf
from apps.attendance.models import AttendanceRecord, ExamAttendanceStatus
from apps.notifications.models import Announcement
from apps.audit.models import AuditLog, SystemSetting

User = get_user_model()

class ExamForgeIntegratedModulesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin_integ', email='admin_integ@examforge.edu', password='password123', role=UserRole.ADMIN
        )
        self.client.force_authenticate(user=self.admin)

        # Academics & Students
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH-CSE', name='B.Tech CSE', department=self.dept)
        self.branch = Branch.objects.create(code='CSE', name='CSE', course=self.course)
        self.sem = Semester.objects.create(branch=self.branch, semester_number=5)
        self.subj = Subject.objects.create(code='CS501', name='Operating Systems', department=self.dept, branch=self.branch, semester_number=5)

        self.student = Student.objects.create(
            register_number='23CSE099', first_name='Rohan', last_name='Gupta',
            email='rohan@student.examforge.edu', branch=self.branch, current_semester_number=5
        )
        self.reg = SubjectRegistration.objects.create(
            student=self.student, subject=self.subj, eligibility_status=EligibilityStatus.ELIGIBLE
        )

        # Faculty
        self.fac_user = User.objects.create_user(username='fac_test', email='fac@examforge.edu', password='password123', role=UserRole.FACULTY)
        self.fac = FacultyProfile.objects.create(
            user=self.fac_user, employee_id='FAC-CS-99', first_name='Deepak', last_name='Kumar',
            department=self.dept, designation=Designation.PROFESSOR, email='fac@examforge.edu'
        )

        # Infrastructure
        self.block = Block.objects.create(code='NB', name='North Block')
        self.room = Room.objects.create(
            block=self.block, room_number='101', room_type=RoomType.EXAM_HALL, usable_exam_capacity=30
        )
        self.slot = TimeSlot.objects.create(
            code='M1', name='Morning Shift', shift='MORNING',
            start_time=datetime.time(9, 30), end_time=datetime.time(12, 30), duration_minutes=180
        )

        # Session & Timetable
        self.today = datetime.date.today()
        self.session = ExamSession.objects.create(
            code='ESE-INT-2025', name='Integration Test Exam',
            academic_year='2025-2026', start_date=self.today + datetime.timedelta(days=7),
            end_date=self.today + datetime.timedelta(days=14), created_by=self.admin
        )
        self.cfg = ExamSubjectConfig.objects.create(session=self.session, subject=self.subj)
        self.timetable = Timetable.objects.create(session=self.session, version='1.0', status='VALIDATED', is_conflict_free=True)
        self.entry = TimetableEntry.objects.create(
            timetable=self.timetable, subject_config=self.cfg, exam_date=self.session.start_date, time_slot=self.slot
        )

    def test_member1_user_authentication_and_faculty(self):
        """Tests Member 1 login API and faculty profile retrieval."""
        response = self.client.post('/api/auth/login/', {
            'username_or_email': 'admin_integ',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

        fac_resp = self.client.get('/api/faculty/profiles/')
        self.assertEqual(fac_resp.status_code, 200)
        self.assertGreaterEqual(len(fac_resp.data['results']), 1)

    def test_member2_student_bulk_csv_import(self):
        """Tests Member 2 student CSV bulk import with duplicate detection."""
        csv_data = "register_number,first_name,last_name,email,branch_code,semester\n" \
                   "23CSE101,John,Doe,john.doe@examforge.edu,CSE,5\n" \
                   "23CSE099,Rohan,Gupta,rohan@student.examforge.edu,CSE,5\n"  # duplicate
        
        response = self.client.post('/api/students/records/bulk-import/', {
            'csv_content': csv_data
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_imported'], 1)
        self.assertEqual(response.data['total_duplicates'], 1)

    def test_member4_seating_allocation_and_invigilation(self):
        """Tests Member 4 auto-allocation of seats and faculty assignment."""
        alloc_resp = self.client.post('/api/seating/plans/auto-allocate/', {
            'session_id': self.session.id,
            'exam_date': str(self.session.start_date),
            'time_slot_id': self.slot.id
        })
        self.assertEqual(alloc_resp.status_code, 200)
        self.assertTrue(alloc_resp.data['success'])

        # Auto-assign invigilator
        invig_resp = self.client.post('/api/invigilation/duties/auto-assign/', {
            'session_id': self.session.id
        })
        self.assertEqual(invig_resp.status_code, 200)
        self.assertTrue(invig_resp.data['success'])

    def test_member5_hallticket_and_pdf_generation(self):
        """Tests Member 5 hall ticket issuance and PDF generation."""
        # Approve and publish session first
        self.session.status = 'PUBLISHED'
        self.session.save()

        gen_resp = self.client.post('/api/halltickets/passes/generate-bulk/', {
            'session_id': self.session.id
        })
        self.assertEqual(gen_resp.status_code, 200)
        
        ht = HallTicket.objects.filter(session=self.session, student=self.student).first()
        self.assertIsNotNone(ht)

        # Test local PDF generation
        pdf_bytes = generate_hall_ticket_pdf(ht)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b'%PDF-'))

    def test_member5_attendance_recording(self):
        """Tests Member 5 exam attendance marking."""
        att = AttendanceRecord.objects.create(
            session=self.session,
            timetable_entry=self.entry,
            student=self.student,
            room=self.room,
            status=ExamAttendanceStatus.PRESENT,
            answer_booklet_number='BK-9901'
        )
        self.assertEqual(att.status, ExamAttendanceStatus.PRESENT)

    def test_dashboard_analytics_overview(self):
        """Tests Member 5 / analytics dashboard API."""
        resp = self.client.get('/api/analytics/dashboard/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data['success'])
        self.assertIn('readiness_score', resp.data['summary'])
