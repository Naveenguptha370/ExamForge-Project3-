from django.test import TestCase
from datetime import date, time
from academics.models import Department, Subject
from examinations.models import ExamSession, TimeSlot, Examination
from infrastructure.models import Building, Room, RoomMaintenance, RoomAssignment
from infrastructure.services import ensure_room_seats, check_room_availability, get_room_utilization_stats


class InfrastructureTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.building = Building.objects.create(code='ARYA', name='Aryabhata Block')
        self.room = Room.objects.create(
            building=self.building,
            room_number='A-101',
            floor=1,
            capacity=30,
            usable_capacity=24,
            rows=6,
            columns=5
        )
        self.session = ExamSession.objects.create(
            name='Spring 2026',
            start_date=date(2026, 10, 15),
            end_date=date(2026, 10, 25)
        )
        self.slot = TimeSlot.objects.create(
            name='Morning',
            start_time=time(9, 30),
            end_time=time(12, 30)
        )
        self.subject = Subject.objects.create(code='CS101', name='Intro to CS', department=self.dept)
        self.exam = Examination.objects.create(
            session=self.session,
            subject=self.subject,
            exam_date=date(2026, 10, 15),
            time_slot=self.slot
        )

    def test_ensure_room_seats_creation(self):
        ensure_room_seats(self.room)
        seats_count = self.room.seats.count()
        self.assertEqual(seats_count, 30)  # 6 rows * 5 cols = 30 seats

    def test_room_maintenance_blocks_availability(self):
        RoomMaintenance.objects.create(
            room=self.room,
            start_date=date(2026, 10, 14),
            end_date=date(2026, 10, 16),
            reason='Floor repair'
        )
        is_avail, reason = check_room_availability(self.room.id, date(2026, 10, 15), self.slot.id)
        self.assertFalse(is_avail)
        self.assertIn("maintenance", reason.lower())

    def test_overlapping_exam_assignment_blocks_availability(self):
        RoomAssignment.objects.create(
            examination=self.exam,
            room=self.room,
            allotted_students_count=20
        )
        is_avail, reason = check_room_availability(self.room.id, date(2026, 10, 15), self.slot.id)
        self.assertFalse(is_avail)
        self.assertIn("already assigned", reason.lower())

    def test_utilization_stats(self):
        stats = get_room_utilization_stats()
        self.assertEqual(stats['total_rooms'], 1)
        self.assertEqual(stats['total_usable_capacity'], 24)
