import datetime
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import UserRole
from apps.academics.models import Department, Course, Branch, Semester, Subject, DifficultyLevel, SubjectType
from apps.students.models import Student, SubjectRegistration, EligibilityStatus
from apps.examinations.models import ExamSession, TimeSlot, ExamSubjectConfig, SchedulingConstraintConfig, SessionStatus
from apps.scheduling.models import Timetable, TimetableEntry, SchedulingClash, ClashSeverity, ClashType, TimetableRevision
from apps.scheduling.engine.solver import ConstraintTimetableSolver, SolverOutcome
from apps.scheduling.engine.conflict_analyzer import ConflictAnalyzer
from apps.scheduling.engine.pdf_exporter import generate_timetable_pdf

User = get_user_model()

class Member3SchedulingTests(TestCase):
    def setUp(self):
        # 1. Users
        self.admin = User.objects.create_superuser(
            username='admin_test',
            email='admin_test@examforge.edu',
            password='password123',
            role=UserRole.ADMIN
        )
        self.student_user = User.objects.create_user(
            username='student_test',
            email='student_test@examforge.edu',
            password='password123',
            role=UserRole.STUDENT
        )

        # 2. Academics
        self.dept = Department.objects.create(code='CSE', name='Computer Science & Engineering')
        self.course = Course.objects.create(code='BTECH-CSE', name='B.Tech CSE', department=self.dept)
        self.branch = Branch.objects.create(code='CSE', name='Computer Science & Engineering', course=self.course)
        self.sem = Semester.objects.create(branch=self.branch, semester_number=5, academic_year='2025-2026')

        self.subj1 = Subject.objects.create(
            code='CS501', name='Operating Systems', department=self.dept, branch=self.branch,
            semester_number=5, difficulty=DifficultyLevel.HARD, credits=4.0
        )
        self.subj2 = Subject.objects.create(
            code='CS502', name='Database Management Systems', department=self.dept, branch=self.branch,
            semester_number=5, difficulty=DifficultyLevel.MEDIUM, credits=4.0
        )
        self.subj3 = Subject.objects.create(
            code='CS503', name='Theory of Computation', department=self.dept, branch=self.branch,
            semester_number=5, difficulty=DifficultyLevel.HARD, credits=3.0
        )

        # 3. Students
        self.student1 = Student.objects.create(
            register_number='23CSE001', first_name='Alice', last_name='Smith',
            email='alice@student.examforge.edu', branch=self.branch, current_semester_number=5
        )
        self.student2 = Student.objects.create(
            register_number='23CSE002', first_name='Bob', last_name='Jones',
            email='bob@student.examforge.edu', branch=self.branch, current_semester_number=5
        )

        # Enrolls in subj1 & subj2
        SubjectRegistration.objects.create(student=self.student1, subject=self.subj1, eligibility_status=EligibilityStatus.ELIGIBLE)
        SubjectRegistration.objects.create(student=self.student1, subject=self.subj2, eligibility_status=EligibilityStatus.ELIGIBLE)
        SubjectRegistration.objects.create(student=self.student2, subject=self.subj1, eligibility_status=EligibilityStatus.ELIGIBLE)

        # 4. Time Slots
        self.slot1 = TimeSlot.objects.create(
            code='M1', name='Morning Shift (09:30 AM - 12:30 PM)', shift='MORNING',
            start_time=datetime.time(9, 30), end_time=datetime.time(12, 30), duration_minutes=180, sort_order=1
        )
        self.slot2 = TimeSlot.objects.create(
            code='A1', name='Afternoon Shift (01:30 PM - 04:30 PM)', shift='AFTERNOON',
            start_time=datetime.time(13, 30), end_time=datetime.time(16, 30), duration_minutes=180, sort_order=2
        )

        # 5. Exam Session
        self.today = datetime.date.today()
        self.session = ExamSession.objects.create(
            code='TEST-ESE-2025', name='Test End Semester Examination',
            academic_year='2025-2026', term='ODD',
            start_date=self.today + datetime.timedelta(days=7),
            end_date=self.today + datetime.timedelta(days=21),
            status=SessionStatus.DRAFT,
            created_by=self.admin
        )

        self.constraints = SchedulingConstraintConfig.objects.create(
            session=self.session,
            max_exams_per_student_per_day=1,
            min_study_gap_days_hard=1,
            prevent_cross_branch_clashes=True,
            allow_saturday_exams=True,
            allow_sunday_exams=False
        )

        self.cfg1 = ExamSubjectConfig.objects.create(session=self.session, subject=self.subj1, expected_students_count=60)
        self.cfg2 = ExamSubjectConfig.objects.create(session=self.session, subject=self.subj2, expected_students_count=60)
        self.cfg3 = ExamSubjectConfig.objects.create(session=self.session, subject=self.subj3, expected_students_count=60)

    def test_csp_solver_generates_successful_timetable(self):
        """Tests that the CSP solver places all subjects without hard clashes."""
        solver = ConstraintTimetableSolver(exam_session=self.session, user=self.admin)
        result = solver.solve()

        self.assertEqual(result.outcome, SolverOutcome.SUCCESS)
        self.assertEqual(result.total_scheduled, 3)
        self.assertIsNotNone(result.timetable)
        self.assertTrue(result.timetable.is_conflict_free)
        self.assertEqual(result.timetable.status, 'VALIDATED')

        # Check that all 3 entries are created on distinct days (due to 1 exam/day rule for same branch)
        dates = list(result.timetable.entries.values_list('exam_date', flat=True))
        self.assertEqual(len(dates), 3)
        self.assertEqual(len(set(dates)), 3)

    def test_conflict_analyzer_detects_student_double_booking(self):
        """Tests that forcing two subjects with shared students into the same slot creates a CRITICAL clash."""
        timetable = Timetable.objects.create(session=self.session, version='1.0', status='DRAFT')
        
        # Force CS501 and CS502 into the same date and slot
        clash_date = self.session.start_date
        TimetableEntry.objects.create(timetable=timetable, subject_config=self.cfg1, exam_date=clash_date, time_slot=self.slot1)
        TimetableEntry.objects.create(timetable=timetable, subject_config=self.cfg2, exam_date=clash_date, time_slot=self.slot1)

        analyzer = ConflictAnalyzer(timetable)
        audit = analyzer.analyze()

        self.assertFalse(audit['is_conflict_free'])
        self.assertGreaterEqual(audit['critical_count'], 1)
        self.assertTrue(SchedulingClash.objects.filter(timetable=timetable, severity=ClashSeverity.CRITICAL).exists())

    def test_solver_reports_infeasible_when_date_window_is_too_small(self):
        """Tests that solver handles impossible constraints gracefully."""
        # 1-day session for 3 branch exams (impossible with 1 exam/day constraint)
        impossible_session = ExamSession.objects.create(
            code='IMPOSSIBLE-2025', name='Impossible Exam',
            academic_year='2025-2026',
            start_date=self.today,
            end_date=self.today,
            status=SessionStatus.DRAFT,
            created_by=self.admin
        )
        SchedulingConstraintConfig.objects.create(session=impossible_session, max_exams_per_student_per_day=1)
        ExamSubjectConfig.objects.create(session=impossible_session, subject=self.subj1)
        ExamSubjectConfig.objects.create(session=impossible_session, subject=self.subj2)
        ExamSubjectConfig.objects.create(session=impossible_session, subject=self.subj3)

        solver = ConstraintTimetableSolver(exam_session=impossible_session, user=self.admin)
        result = solver.solve()

        # Should be PARTIAL or INFEASIBLE, never silently successful
        self.assertIn(result.outcome, [SolverOutcome.PARTIAL, SolverOutcome.INFEASIBLE])
        self.assertFalse(impossible_session.timetable.is_conflict_free)

    def test_manual_override_and_version_tracking(self):
        """Tests that manual overrides update the entry, bump the version, and log a revision."""
        solver = ConstraintTimetableSolver(exam_session=self.session, user=self.admin)
        result = solver.solve()
        timetable = result.timetable

        entry = timetable.entries.first()
        old_date = entry.exam_date
        new_date = old_date + datetime.timedelta(days=1)

        # Update entry
        entry.exam_date = new_date
        entry.is_manual_override = True
        entry.save()

        # Update version and create revision
        timetable.version = '1.1'
        timetable.save()
        TimetableRevision.objects.create(
            timetable=timetable,
            revision_number='1.1',
            author=self.admin,
            change_summary=f"Rescheduled {entry.subject_config.subject.code} to {new_date}."
        )

        self.assertEqual(timetable.revisions.count(), 2)  # initial solver + manual revision
        self.assertEqual(timetable.version, '1.1')

    def test_pdf_timetable_generation(self):
        """Tests that ReportLab locally generates valid PDF binary content."""
        solver = ConstraintTimetableSolver(exam_session=self.session, user=self.admin)
        result = solver.solve()
        timetable = result.timetable

        pdf_bytes = generate_timetable_pdf(timetable)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(pdf_bytes.startswith(b'%PDF-'))
        self.assertGreater(len(pdf_bytes), 1000)
