from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, time
from academics.models import Department, Subject, Faculty, FacultyLeave
from examinations.models import ExamSession, TimeSlot, Examination
from infrastructure.models import Building, Room, RoomAssignment
from invigilation.models import InvigilatorDuty
from invigilation.engine import InvigilatorAllocationEngine


class InvigilationTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.subject = Subject.objects.create(code='CS301', name='Algorithms', department=self.dept)
        self.building = Building.objects.create(code='B1', name='Block 1')
        self.room1 = Room.objects.create(building=self.building, room_number='R1', floor=1, capacity=30, usable_capacity=25, rows=5, columns=5)
        self.room2 = Room.objects.create(building=self.building, room_number='R2', floor=1, capacity=30, usable_capacity=25, rows=5, columns=5)

        self.session = ExamSession.objects.create(name='Spring 2026', start_date=date(2026, 10, 15), end_date=date(2026, 10, 25))
        self.slot = TimeSlot.objects.create(name='Morning Slot', start_time=time(9, 30), end_time=time(12, 30))
        self.exam = Examination.objects.create(
            session=self.session,
            subject=self.subject,
            exam_date=date(2026, 10, 15),
            time_slot=self.slot
        )

        RoomAssignment.objects.create(examination=self.exam, room=self.room1, allotted_students_count=20)
        RoomAssignment.objects.create(examination=self.exam, room=self.room2, allotted_students_count=20)

        # Create 3 faculty members
        self.f1 = Faculty.objects.create(employee_id='F1', name='Faculty 1', email='f1@exam.edu', department=self.dept)
        self.f2 = Faculty.objects.create(employee_id='F2', name='Faculty 2', email='f2@exam.edu', department=self.dept)
        self.f3 = Faculty.objects.create(employee_id='F3', name='Faculty 3', email='f3@exam.edu', department=self.dept)

    def test_auto_allocation_and_conflict_free(self):
        res = InvigilatorAllocationEngine.allocate(self.exam.id, ratio_per_students=30)
        self.assertEqual(res['total_needed'], 2)
        self.assertEqual(res['total_assigned'], 2)
        self.assertTrue(res['is_fully_staffed'])
        self.assertEqual(InvigilatorDuty.objects.filter(examination=self.exam).count(), 2)

    def test_leave_prevents_duty_assignment(self):
        # Put F1 and F2 on leave
        FacultyLeave.objects.create(faculty=self.f1, start_date=date(2026, 10, 14), end_date=date(2026, 10, 16), reason='Medical')
        FacultyLeave.objects.create(faculty=self.f2, start_date=date(2026, 10, 14), end_date=date(2026, 10, 16), reason='Conference')

        # Only F3 is available, but 2 rooms need invigilators!
        res = InvigilatorAllocationEngine.allocate(self.exam.id, ratio_per_students=30)
        self.assertEqual(res['total_assigned'], 1)
        self.assertFalse(res['is_fully_staffed'])
        self.assertEqual(len(res['unstaffed_rooms']), 1)
        self.assertEqual(res['unstaffed_rooms'][0]['shortage'], 1)

    def test_manual_reassign_blocks_overlap(self):
        res = InvigilatorAllocationEngine.allocate(self.exam.id, ratio_per_students=30)
        duties = list(InvigilatorDuty.objects.filter(examination=self.exam))
        duty1, duty2 = duties[0], duties[1]

        # Try to reassign duty1 to duty2's faculty (would cause duplicate in same slot)
        with self.assertRaises(ValidationError):
            InvigilatorAllocationEngine.reassign_duty(duty1.id, duty2.faculty.id)
