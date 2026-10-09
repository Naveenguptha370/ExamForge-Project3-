from datetime import date, time
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.infrastructure.models import Building, ExaminationRoom
from apps.seating.models import Seat, SeatingPlan, SeatAllocation
from apps.invigilation.models import InvigilatorDuty
from apps.faculty.models import FacultyProfile
from apps.academics.models import Department, Course, Semester, Subject
from apps.students.models import StudentProfile
from apps.examinations.models import ExamSession, ExamSubject

User = get_user_model()

class Member4InfrastructureSeatingTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH', name='B.Tech', department=self.dept)
        self.sem = Semester.objects.create(number=4, academic_year='2025-2026')
        self.subject = Subject.objects.create(code='CS401', name='Algorithms', department=self.dept, semester=self.sem)

        self.bldg = Building.objects.create(code='B1', name='Main Block')
        self.room = ExaminationRoom.objects.create(
            room_number='LH-101',
            building=self.bldg,
            rows=2,
            columns=2,
            total_capacity=4,
            usable_capacity=2
        )

        self.session = ExamSession.objects.create(
            session_code='ESE-MAY',
            name='May Session',
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 20)
        )
        self.es = ExamSubject.objects.create(exam_session=self.session, subject=self.subject)

        # Create seats
        self.seat1 = Seat.objects.create(room=self.room, row_num=1, col_num=1, seat_label='A1')
        self.seat2 = Seat.objects.create(room=self.room, row_num=1, col_num=2, seat_label='A2')

        self.student1 = StudentProfile.objects.create(
            registration_no='R1', roll_no='24CS01', first_name='S1', last_name='L1', email='s1@t.edu',
            department=self.dept, course=self.course, semester=self.sem
        )
        self.student2 = StudentProfile.objects.create(
            registration_no='R2', roll_no='24CS02', first_name='S2', last_name='L2', email='s2@t.edu',
            department=self.dept, course=self.course, semester=self.sem
        )

    def test_seating_plan_allocations_and_uniqueness(self):
        plan = SeatingPlan.objects.create(exam_subject=self.es, room=self.room)

        # Allocate student 1 to seat 1
        alloc1 = SeatAllocation.objects.create(seating_plan=plan, seat=self.seat1, student=self.student1)
        self.assertEqual(alloc1.student.roll_no, '24CS01')

        # Attempt duplicate seat allocation to another student in same plan -> should fail!
        with self.assertRaises(Exception):
            SeatAllocation.objects.create(seating_plan=plan, seat=self.seat1, student=self.student2)

        # Attempt assigning same student two seats in same plan -> should fail!
        with self.assertRaises(Exception):
            SeatAllocation.objects.create(seating_plan=plan, seat=self.seat2, student=self.student1)
