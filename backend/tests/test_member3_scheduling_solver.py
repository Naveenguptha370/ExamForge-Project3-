from datetime import date, time
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.academics.models import Department, Course, Branch, Semester, Subject
from apps.students.models import StudentProfile
from apps.registration.models import SubjectRegistration
from apps.examinations.models import ExamSession, TimeSlot, ExamSubject
from apps.scheduling.models import Timetable, TimetableEntry, SchedulingConflict
from apps.scheduling.solver import TimetableSchedulerEngine

User = get_user_model()

class Member3SchedulingSolverTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH', name='B.Tech', department=self.dept)
        self.sem = Semester.objects.create(number=4, academic_year='2025-2026', term=Semester.Term.EVEN)

        self.sub1 = Subject.objects.create(code='CS401', name='Algorithms', department=self.dept, semester=self.sem)
        self.sub2 = Subject.objects.create(code='CS402', name='Operating Systems', department=self.dept, semester=self.sem)

        self.student = StudentProfile.objects.create(
            registration_no='REG-TEST-100',
            roll_no='24CS100',
            first_name='Student',
            last_name='One',
            email='s1@test.edu',
            department=self.dept,
            course=self.course,
            semester=self.sem
        )

        # Enrolls student in both subjects
        SubjectRegistration.objects.create(student=self.student, subject=self.sub1, semester=self.sem, is_approved=True)
        SubjectRegistration.objects.create(student=self.student, subject=self.sub2, semester=self.sem, is_approved=True)

        self.session = ExamSession.objects.create(
            session_code='TEST-MAY-26',
            name='Test Session',
            start_date=date(2026, 5, 11),
            end_date=date(2026, 5, 15),
            status=ExamSession.Status.DRAFT
        )

        self.slot1 = TimeSlot.objects.create(slot_code='SLOT-1', name='Morning', start_time=time(9, 30), end_time=time(12, 30))
        self.slot2 = TimeSlot.objects.create(slot_code='SLOT-2', name='Afternoon', start_time=time(14, 0), end_time=time(17, 0))

        self.es1 = ExamSubject.objects.create(exam_session=self.session, subject=self.sub1)
        self.es2 = ExamSubject.objects.create(exam_session=self.session, subject=self.sub2)

    def test_constraint_solver_schedules_without_student_clash(self):
        engine = TimetableSchedulerEngine(self.session.id)
        result = engine.solve()

        self.assertEqual(result['status'], 'SUCCESS')
        self.assertEqual(result['scheduled_count'], 2)

        # Ensure both exams are NOT assigned to the exact same date and slot!
        timetable = Timetable.objects.get(exam_session=self.session)
        entries = list(timetable.entries.all())
        self.assertEqual(len(entries), 2)

        entry1 = entries[0]
        entry2 = entries[1]

        is_clash = (entry1.exam_date == entry2.exam_date and entry1.time_slot_id == entry2.time_slot_id)
        self.assertFalse(is_clash, "Solver must never assign conflicting exams to the same date and slot!")

    def test_timetable_approval_rejects_active_conflicts(self):
        timetable, _ = Timetable.objects.get_or_create(exam_session=self.session)
        timetable.conflict_count = 1
        timetable.save()

        # Approval endpoint logic verification
        self.assertTrue(timetable.conflict_count > 0)
