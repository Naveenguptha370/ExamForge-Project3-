from django.test import TestCase
from datetime import date, time
from academics.models import Department, Course, Subject, Student
from examinations.models import ExamSession, TimeSlot, Examination, ExamRegistration
from infrastructure.models import Building, Room
from infrastructure.services import ensure_room_seats
from seating.models import SeatingPlan, Seat, SeatAllocation
from seating.engine import SeatingEngine


class SeatingTests(TestCase):
    def setUp(self):
        self.dept_cs = Department.objects.create(code='CSE', name='Computer Science')
        self.dept_ec = Department.objects.create(code='ECE', name='Electronics')
        self.course_cs = Course.objects.create(code='BCS', name='BTech CS', department=self.dept_cs)
        self.course_ec = Course.objects.create(code='BEC', name='BTech EC', department=self.dept_ec)
        self.subject = Subject.objects.create(code='CS201', name='Data Structures', department=self.dept_cs)
        
        self.building = Building.objects.create(code='B1', name='Main Block')
        self.room = Room.objects.create(
            building=self.building,
            room_number='101',
            floor=1,
            capacity=20,
            usable_capacity=16,
            rows=4,
            columns=4
        )
        ensure_room_seats(self.room)

        self.session = ExamSession.objects.create(name='Fall 2026', start_date=date(2026, 11, 1), end_date=date(2026, 11, 10))
        self.slot = TimeSlot.objects.create(name='Morning', start_time=time(9, 30), end_time=time(12, 30))
        self.exam = Examination.objects.create(
            session=self.session,
            subject=self.subject,
            exam_date=date(2026, 11, 2),
            time_slot=self.slot
        )

        # Create 10 students (5 CSE, 5 ECE)
        self.students = []
        for i in range(1, 6):
            s = Student.objects.create(
                registration_no=f"REG-CS-{i}",
                roll_no=f"CS{i:02d}",
                name=f"CS Student {i}",
                department=self.dept_cs,
                course=self.course_cs
            )
            ExamRegistration.objects.create(examination=self.exam, student=s)
            self.students.append(s)

        for i in range(1, 6):
            s = Student.objects.create(
                registration_no=f"REG-EC-{i}",
                roll_no=f"EC{i:02d}",
                name=f"EC Student {i}",
                department=self.dept_ec,
                course=self.course_ec
            )
            ExamRegistration.objects.create(examination=self.exam, student=s)
            self.students.append(s)

    def test_seating_generation_department_separated(self):
        result = SeatingEngine.generate(
            examination_id=self.exam.id,
            room_ids=[self.room.id],
            spacing_rule='department_separated'
        )
        self.assertEqual(result['total_allocated'], 10)
        self.assertEqual(result['capacity_shortage'], 0)
        self.assertEqual(SeatAllocation.objects.filter(examination=self.exam).count(), 10)

    def test_seating_uniqueness_and_revalidation(self):
        SeatingEngine.generate(
            examination_id=self.exam.id,
            room_ids=[self.room.id],
            spacing_rule='consecutive'
        )
        val = SeatingEngine.revalidate(self.exam.id)
        self.assertTrue(val['is_valid'])
        self.assertEqual(len(val['issues']), 0)

    def test_capacity_shortage_detection(self):
        # Create small room with only 4 seats
        small_room = Room.objects.create(
            building=self.building,
            room_number='TINY',
            floor=1,
            capacity=4,
            usable_capacity=4,
            rows=2,
            columns=2
        )
        ensure_room_seats(small_room)

        # Attempt to seat 10 students in a 4-seat room
        result = SeatingEngine.generate(
            examination_id=self.exam.id,
            room_ids=[small_room.id],
            spacing_rule='consecutive'
        )
        self.assertEqual(result['total_allocated'], 4)
        self.assertEqual(result['total_unallocated'], 6)
        self.assertEqual(result['capacity_shortage'], 6)
        self.assertIn("Shortage", result['validation_status'])

    def test_manual_seat_swap(self):
        SeatingEngine.generate(
            examination_id=self.exam.id,
            room_ids=[self.room.id],
            spacing_rule='consecutive'
        )
        allocs = list(SeatAllocation.objects.filter(examination=self.exam)[:2])
        alloc1, alloc2 = allocs[0], allocs[1]
        student1, student2 = alloc1.student, alloc2.student
        seat1, seat2 = alloc1.seat, alloc2.seat

        swap_res = SeatingEngine.swap_or_move(alloc1.id, self.room.id, seat2.id)
        self.assertTrue(swap_res['success'])

        alloc1.refresh_from_db()
        alloc2.refresh_from_db()
        self.assertEqual(alloc1.seat_id, seat2.id)
        self.assertEqual(alloc2.seat_id, seat1.id)
