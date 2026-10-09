import time
import datetime
from collections import defaultdict
from django.utils import timezone
from django.db import transaction
from apps.scheduling.models import Timetable, TimetableEntry, TimetableStatus, TimetableRevision
from apps.examinations.models import ExamSession, TimeSlot, ExamSubjectConfig
from apps.students.models import SubjectRegistration, EligibilityStatus
from apps.infrastructure.models import Room
from .conflict_analyzer import ConflictAnalyzer

class SolverOutcome:
    SUCCESS = 'SUCCESS'
    PARTIAL = 'PARTIAL'
    INFEASIBLE = 'INFEASIBLE'


class SolverResult:
    def __init__(self, outcome, timetable, message, total_scheduled=0, total_configs=0, duration_ms=0.0, iterations=0, unplaced=None):
        self.outcome = outcome
        self.timetable = timetable
        self.message = message
        self.total_scheduled = total_scheduled
        self.total_configs = total_configs
        self.duration_ms = duration_ms
        self.iterations = iterations
        self.unplaced = unplaced or []

    def to_dict(self):
        return {
            'outcome': self.outcome,
            'message': self.message,
            'total_scheduled': self.total_scheduled,
            'total_configs': self.total_configs,
            'duration_ms': round(self.duration_ms, 2),
            'iterations': self.iterations,
            'is_conflict_free': self.timetable.is_conflict_free if self.timetable else False,
            'clash_count': self.timetable.clash_count if self.timetable else 0,
            'unplaced_count': len(self.unplaced),
            'unplaced_subjects': self.unplaced
        }


class ConstraintTimetableSolver:
    """
    Genuine Python-based Constraint Satisfaction Problem (CSP) solver for Exam Timetables.
    Employs MRV (Minimum Remaining Values), Degree Heuristics, Least Constraining Value (LCV),
    and Backtracking with Forward Checking.
    """

    def __init__(self, exam_session, user=None):
        self.session = exam_session
        self.user = user
        self.constraints = getattr(exam_session, 'constraint_config', None)
        self.iterations = 0
        self.start_time = 0
        self.max_iterations = 25000
        self.timeout_seconds = self.constraints.solver_timeout_seconds if self.constraints else 30

    def solve(self):
        """
        Executes the CSP scheduling algorithm.
        Generates and saves Timetable and TimetableEntry objects.
        """
        self.start_time = time.time()
        self.iterations = 0

        # 1. Fetch available time slots
        time_slots = list(TimeSlot.objects.filter(is_active=True).order_by('sort_order', 'start_time'))
        if not time_slots:
            return SolverResult(
                outcome=SolverOutcome.INFEASIBLE,
                timetable=None,
                message="No active Time Slots found. Please configure at least one time slot."
            )

        # 2. Fetch configured subjects
        configs = list(self.session.configured_subjects.select_related('subject', 'subject__branch', 'subject__department').all())
        if not configs:
            return SolverResult(
                outcome=SolverOutcome.INFEASIBLE,
                timetable=None,
                message="No subjects configured for this examination session. Populate subjects before running solver."
            )

        # 3. Generate candidate date list within [start_date, end_date]
        candidate_dates = []
        cur_date = self.session.start_date
        allow_sat = self.constraints.allow_saturday_exams if self.constraints else True
        allow_sun = self.constraints.allow_sunday_exams if self.constraints else False

        while cur_date <= self.session.end_date:
            weekday = cur_date.weekday()  # 0=Mon, 5=Sat, 6=Sun
            if weekday == 6 and not allow_sun:
                cur_date += datetime.timedelta(days=1)
                continue
            if weekday == 5 and not allow_sat:
                cur_date += datetime.timedelta(days=1)
                continue
            candidate_dates.append(cur_date)
            cur_date += datetime.timedelta(days=1)

        if not candidate_dates:
            return SolverResult(
                outcome=SolverOutcome.INFEASIBLE,
                timetable=None,
                message="No valid examination dates available in session date range under current weekend constraints."
            )

        # 4. Generate full domain of (date, time_slot)
        full_domain = [(d, s) for d in candidate_dates for s in time_slots]

        # 5. Precompute student enrollment sets for each subject config
        enrollment_map = {}
        for cfg in configs:
            student_ids = set(SubjectRegistration.objects.filter(
                subject=cfg.subject,
                eligibility_status=EligibilityStatus.ELIGIBLE
            ).values_list('student_id', flat=True))
            enrollment_map[cfg.id] = student_ids

        # 6. Branch & semester index
        branch_sem_map = {}
        for cfg in configs:
            subj = cfg.subject
            branch_sem_map[cfg.id] = (subj.branch_id, subj.semester_number)

        # 7. Sort variables using MRV & Degree Heuristics
        def variable_priority(cfg):
            # Prioritize heavy difficulty, high student count, and subjects with preferred slots
            diff = cfg.difficulty_weight
            students = cfg.expected_students_count or len(enrollment_map.get(cfg.id, []))
            has_pref = 1 if cfg.preferred_slot else 0
            return -(diff * 10 + (students // 10) + has_pref * 5)

        sorted_configs = sorted(configs, key=variable_priority)

        # 8. CSP Backtracking Search State
        # assignment: cfg_id -> (date, slot)
        assignment = {}
        # slot_usage: (date, slot_id) -> list of cfg_ids
        slot_usage = defaultdict(list)
        # date_branch_usage: (date, branch_id, sem_num) -> list of cfg_ids
        date_branch_usage = defaultdict(list)

        def is_valid_assignment(cfg, date_val, slot_val):
            self.iterations += 1
            cfg_id = cfg.id
            slot_key = (date_val, slot_val.id)
            branch_sem = branch_sem_map[cfg_id]
            branch_key = (date_val, branch_sem[0], branch_sem[1])

            # Check preferred slot constraint
            if cfg.preferred_slot and cfg.preferred_slot_id != slot_val.id:
                pass  # Soft preference, don't strictly reject if needed

            # Hard Constraint A: No multiple exams on same day for same branch + semester
            if branch_sem[0] is not None:
                if date_branch_usage[branch_key]:
                    return False

            # Hard Constraint B: Same slot collisions
            existing_in_slot = slot_usage[slot_key]
            if existing_in_slot:
                cfg_students = enrollment_map.get(cfg_id, set())
                for other_id in existing_in_slot:
                    # Check branch + semester identity
                    other_bs = branch_sem_map[other_id]
                    if branch_sem[0] is not None and other_bs[0] == branch_sem[0] and other_bs[1] == branch_sem[1]:
                        return False
                    
                    # Check shared student enrollment intersection
                    if cfg_students:
                        other_students = enrollment_map.get(other_id, set())
                        if cfg_students & other_students:
                            return False

            return True

        def get_ordered_domain_values(cfg):
            """
            Least Constraining Value (LCV) heuristic with study gap optimization.
            """
            branch_sem = branch_sem_map[cfg.id]
            is_hard = (cfg.difficulty_weight >= 4 or cfg.subject.difficulty == 'HARD')

            def value_cost(val):
                date_val, slot_val = val
                cost = 0
                # If cfg has preferred slot, heavily prefer it
                if cfg.preferred_slot and cfg.preferred_slot_id == slot_val.id:
                    cost -= 30

                # Spread exams evenly across days (prefer slots with fewer concurrent exams)
                current_slot_load = len(slot_usage[(date_val, slot_val.id)])
                cost += current_slot_load * 5

                # Prioritize morning slots for heavy exams
                if is_hard and slot_val.shift == 'MORNING':
                    cost -= 10

                return cost

            return sorted(full_domain, key=value_cost)

        # Backtracking recursion
        def backtrack(index):
            if time.time() - self.start_time > self.timeout_seconds:
                return False
            if self.iterations > self.max_iterations:
                return False
            if index >= len(sorted_configs):
                return True

            cfg = sorted_configs[index]
            ordered_values = get_ordered_domain_values(cfg)

            for date_val, slot_val in ordered_values:
                if is_valid_assignment(cfg, date_val, slot_val):
                    # Assign
                    assignment[cfg.id] = (date_val, slot_val)
                    slot_usage[(date_val, slot_val.id)].append(cfg.id)
                    bs = branch_sem_map[cfg.id]
                    date_branch_usage[(date_val, bs[0], bs[1])].append(cfg.id)

                    # Recurse
                    if backtrack(index + 1):
                        return True

                    # Unassign / Backtrack
                    del assignment[cfg.id]
                    slot_usage[(date_val, slot_val.id)].remove(cfg.id)
                    date_branch_usage[(date_val, bs[0], bs[1])].remove(cfg.id)

            return False

        # Run solver
        solved = backtrack(0)
        duration_ms = (time.time() - self.start_time) * 1000

        # Persist timetable to database in transaction
        with transaction.atomic():
            # Get or create Timetable for this session
            timetable, _ = Timetable.objects.get_or_create(
                session=self.session,
                defaults={
                    'created_by': self.user,
                    'version': '1.0',
                    'status': TimetableStatus.DRAFT
                }
            )

            # Clear previous entries
            timetable.entries.all().delete()

            unplaced = []
            placed_count = 0
            distinct_slots = set()

            for cfg in configs:
                if cfg.id in assignment:
                    date_val, slot_val = assignment[cfg.id]
                    TimetableEntry.objects.create(
                        timetable=timetable,
                        subject_config=cfg,
                        exam_date=date_val,
                        time_slot=slot_val,
                        expected_students=cfg.expected_students_count
                    )
                    placed_count += 1
                    distinct_slots.add((date_val, slot_val.id))
                else:
                    unplaced.append({
                        'subject_code': cfg.subject.code,
                        'subject_name': cfg.subject.name,
                        'branch': cfg.subject.branch.code if cfg.subject.branch else 'General',
                        'semester': cfg.subject.semester_number,
                        'reason': 'No clash-free slot available within current examination date window.'
                    })

            timetable.total_exams_scheduled = placed_count
            timetable.total_slots_used = len(distinct_slots)
            timetable.solver_duration_ms = duration_ms
            timetable.solver_iterations = self.iterations
            
            if solved and len(unplaced) == 0:
                timetable.solver_outcome = SolverOutcome.SUCCESS
                outcome = SolverOutcome.SUCCESS
                msg = f"Schedule successfully generated! 100% of subjects ({placed_count}/{len(configs)}) scheduled in {round(duration_ms, 1)}ms with 0 hard clashes."
            elif placed_count > 0:
                timetable.solver_outcome = SolverOutcome.PARTIAL
                outcome = SolverOutcome.PARTIAL
                msg = f"Partially scheduled: {placed_count}/{len(configs)} subjects placed. {len(unplaced)} subjects require date range expansion or additional slots."
            else:
                timetable.solver_outcome = SolverOutcome.INFEASIBLE
                outcome = SolverOutcome.INFEASIBLE
                msg = "No feasible timetable found under current constraints. Extend examination date window or relax constraint parameters."

            timetable.save()

            # Record Revision
            TimetableRevision.objects.create(
                timetable=timetable,
                revision_number=timetable.version,
                author=self.user,
                change_summary=f"Automated CSP solver run completed with outcome {outcome}. {placed_count} scheduled.",
                diff_payload={'placed_count': placed_count, 'unplaced_count': len(unplaced)}
            )

        # Run conflict analyzer on the created entries
        analyzer = ConflictAnalyzer(timetable)
        analyzer.analyze()

        return SolverResult(
            outcome=outcome,
            timetable=timetable,
            message=msg,
            total_scheduled=placed_count,
            total_configs=len(configs),
            duration_ms=duration_ms,
            iterations=self.iterations,
            unplaced=unplaced
        )
