from datetime import date, time
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.academics.models import Department, Course, Semester, Subject
from apps.students.models import StudentProfile
from apps.registration.models import SubjectRegistration
from apps.examinations.models import ExamSession, TimeSlot, ExamSubject
from apps.infrastructure.models import Building, ExaminationRoom
from apps.seating.models import Seat, SeatingPlan, SeatAllocation
from apps.halltickets.models import HallTicket, HallTicketEntry
from apps.halltickets.pdf_generator import generate_hall_ticket_pdf
from apps.attendance.models import ExamAttendanceSheet, AttendanceRecord, AttendanceCorrectionAudit
from apps.system_settings.models import SystemSetting

User = get_user_model()

class Member5DocumentsLifecycleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin_m5', password='Password123!', role=User.Role.ADMIN)
        self.client.force_authenticate(user=self.admin)

        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH', name='B.Tech', department=self.dept)
        self.sem = Semester.objects.create(number=4, academic_year='2025-2026')
        self.subject = Subject.objects.create(code='CS401', name='Algorithms', department=self.dept, semester=self.sem)

        self.bldg = Building.objects.create(code='B1', name='Main Block')
        self.room = ExaminationRoom.objects.create(room_number='LH-101', building=self.bldg, total_capacity=30, usable_capacity=15)
        self.seat = Seat.objects.create(room=self.room, row_num=1, col_num=1, seat_label='A1')

        self.session = ExamSession.objects.create(
            session_code='ESE-2026',
            name='End Semester Exam 2026',
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 20),
            status=ExamSession.Status.PUBLISHED
        )
        self.slot = TimeSlot.objects.create(slot_code='SLOT-M', name='Morning', start_time=time(9, 30), end_time=time(12, 30))
        self.es = ExamSubject.objects.create(exam_session=self.session, subject=self.subject, planned_date=date(2026, 5, 12), time_slot=self.slot)

        self.eligible_student = StudentProfile.objects.create(
            registration_no='REG001', roll_no='24CS001', first_name='Aarav', last_name='Patel',
            email='aarav@test.edu', department=self.dept, course=self.course, semester=self.sem, is_eligible_for_exam=True
        )

        self.ineligible_student = StudentProfile.objects.create(
            registration_no='REG002', roll_no='24CS002', first_name='Rohan', last_name='Shah',
            email='rohan@test.edu', department=self.dept, course=self.course, semester=self.sem, is_eligible_for_exam=False
        )

        # Enroll eligible student with good attendance
        SubjectRegistration.objects.create(student=self.eligible_student, subject=self.subject, semester=self.sem, attendance_percentage=85.0)

    def test_local_pdf_generation_without_external_api(self):
        ticket = HallTicket.objects.create(
            student=self.eligible_student,
            exam_session=self.session,
            ticket_number='HT-TEST-001'
        )
        HallTicketEntry.objects.create(
            hall_ticket=ticket,
            exam_subject=self.es,
            exam_date=date(2026, 5, 12),
            time_slot_str='Morning (09:30 AM - 12:30 PM)',
            room_number='LH-101',
            seat_label='A1'
        )

        pdf_bytes = generate_hall_ticket_pdf(ticket)
        self.assertIsNotNone(pdf_bytes)
        self.assertTrue(pdf_bytes.startswith(b'%PDF'), "PDF output must be a valid binary PDF document!")
        self.assertGreater(len(pdf_bytes), 500)

    def test_hall_ticket_generation_denied_for_ineligible_student(self):
        response = self.client.post('/api/halltickets/tickets/generate_individual/', {
            'student_id': self.ineligible_student.id,
            'exam_session_id': self.session.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ineligible', response.data['error'].lower())

    def test_attendance_recording_and_correction_audit_trail(self):
        sheet = ExamAttendanceSheet.objects.create(exam_subject=self.es, room=self.room)
        record = AttendanceRecord.objects.create(sheet=sheet, student=self.eligible_student, seat_label='A1', status='PRESENT')

        # Correct status from PRESENT to ABSENT
        response = self.client.post(f'/api/attendance/records/{record.id}/correct_status/', {
            'status': 'ABSENT',
            'reason': 'Candidate was mistakenly marked present; actually absent during headcount.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        record.refresh_from_db()
        self.assertEqual(record.status, 'ABSENT')

        # Check audit log creation
        audits = AttendanceCorrectionAudit.objects.filter(attendance_record=record)
        self.assertEqual(audits.count(), 1)
        audit = audits.first()
        self.assertEqual(audit.previous_status, 'PRESENT')
        self.assertEqual(audit.new_status, 'ABSENT')
        self.assertEqual(audit.corrected_by, self.admin)

    def test_readiness_index_endpoint(self):
        response = self.client.get('/api/analytics/reports/readiness_index/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('overall_readiness_score', response.data)
        self.assertIn('phases', response.data)
