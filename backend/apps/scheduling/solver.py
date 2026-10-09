from datetime import timedelta
from collections import defaultdict
from django.db import transaction
from apps.examinations.models import ExamSession, TimeSlot, ExamSubject
from apps.registration.models import SubjectRegistration
from .models import Timetable, TimetableEntry, SchedulingConflict, TimetableRevision

class TimetableSchedulerEngine:
    def __init__(self, exam_session_id):
        self.session = ExamSession.objects.get(id=exam_session_id)
        self.exam_subjects = list(ExamSubject.objects.filter(exam_session=self.session).select_related('subject', 'subject__branch', 'subject__semester'))
        self.time_slots = list(TimeSlot.objects.filter(is_active=True).order_by('start_time'))
        self.enrollments = defaultdict(set)
        self.conflict_graph = defaultdict(set)
        self.max_steps = 5000
        self.steps_taken = 0

    def prepare_data(self):
        # 1. Map each subject to enrolled student IDs
        subject_ids = [es.subject.id for es in self.exam_subjects]
        regs = SubjectRegistration.objects.filter(subject_id__in=subject_ids, is_approved=True).values('subject_id', 'student_id')
        for r in regs:
            self.enrollments[r['subject_id']].add(r['student_id'])

        # 2. Build student conflict graph between exam subjects
        for i in range(len(self.exam_subjects)):
            es1 = self.exam_subjects[i]
            students1 = self.enrollments[es1.subject.id]
            for j in range(i + 1, len(self.exam_subjects)):
                es2 = self.exam_subjects[j]
                students2 = self.enrollments[es2.subject.id]
                shared = students1.intersection(students2)
                if shared:
                    self.conflict_graph[es1.id].add(es2.id)
                    self.conflict_graph[es2.id].add(es1.id)

    def generate_slot_domain(self):
        slots = []
        cur_date = self.session.start_date
        while cur_date <= self.session.end_date:
            # Skip Sundays
            if cur_date.weekday() != 6:
                for ts in self.time_slots:
                    slots.append((cur_date, ts))
            cur_date += timedelta(days=1)
        return slots

    def solve(self):
        self.prepare_data()
        available_slots = self.generate_slot_domain()

        if not available_slots:
            return {
                'status': 'INFEASIBLE',
                'message': 'No available time slots within the session date range (excluding Sundays).',
                'scheduled_count': 0,
                'total_count': len(self.exam_subjects),
                'conflicts': []
            }

        # Sort exam subjects using Most-Constrained-First (MRV) heuristic:
        # Subjects with more student conflicts and more students get scheduled first
        sorted_subjects = sorted(
            self.exam_subjects,
            key=lambda es: (len(self.conflict_graph[es.id]), len(self.enrollments[es.subject.id])),
            reverse=True
        )

        assignment = {}  # exam_subject_id -> (date, time_slot)
        self.steps_taken = 0

        success = self._backtrack(0, sorted_subjects, available_slots, assignment)

        # Save results in database within an atomic transaction
        with transaction.atomic():
            timetable, _ = Timetable.objects.get_or_create(exam_session=self.session)
            timetable.total_subjects_count = len(self.exam_subjects)
            timetable.entries.all().delete()
            timetable.conflicts.all().delete()

            if success:
                # Apply assignments
                for es in self.exam_subjects:
                    date, slot = assignment[es.id]
                    TimetableEntry.objects.create(
                        timetable=timetable,
                        exam_subject=es,
                        exam_date=date,
                        time_slot=slot
                    )
                    es.planned_date = date
                    es.time_slot = slot
                    es.is_scheduled = True
                    es.save()

                timetable.scheduled_count = len(self.exam_subjects)
                timetable.conflict_count = 0
                timetable.status = Timetable.Status.VALIDATED
                timetable.save()

                return {
                    'status': 'SUCCESS',
                    'message': f'Constraint solver successfully scheduled all {len(self.exam_subjects)} examinations without student clashes.',
                    'scheduled_count': len(self.exam_subjects),
                    'total_count': len(self.exam_subjects),
                    'steps': self.steps_taken,
                    'conflicts': []
                }
            else:
                # Partial fallback assignment
                partial_assigned = 0
                conflicts_generated = []

                for es in self.exam_subjects:
                    if es.id in assignment:
                        date, slot = assignment[es.id]
                        TimetableEntry.objects.create(
                            timetable=timetable,
                            exam_subject=es,
                            exam_date=date,
                            time_slot=slot
                        )
                        es.planned_date = date
                        es.time_slot = slot
                        es.is_scheduled = True
                        es.save()
                        partial_assigned += 1
                    else:
                        es.is_scheduled = False
                        es.save()

                        # Identify clashing subject
                        conflicting_ids = self.conflict_graph.get(es.id, set())
                        first_clash_es = None
                        affected_count = 0
                        if conflicting_ids:
                            clash_id = next(iter(conflicting_ids))
                            first_clash_es = next((s for s in self.exam_subjects if s.id == clash_id), None)
                            if first_clash_es:
                                affected_count = len(self.enrollments[es.subject.id].intersection(self.enrollments[first_clash_es.subject.id]))

                        conflict = SchedulingConflict.objects.create(
                            timetable=timetable,
                            conflict_type=SchedulingConflict.ConflictType.STUDENT_CLASH,
                            description=f"Unable to find conflict-free slot for {es.subject.code} within session date boundaries.",
                            exam_subject_1=es,
                            exam_subject_2=first_clash_es,
                            affected_students_count=affected_count
                        )
                        conflicts_generated.append(conflict.description)

                timetable.scheduled_count = partial_assigned
                timetable.conflict_count = len(conflicts_generated)
                timetable.status = Timetable.Status.DRAFT
                timetable.save()

                return {
                    'status': 'PARTIAL',
                    'message': f'Scheduled {partial_assigned}/{len(self.exam_subjects)} subjects. {len(conflicts_generated)} conflict(s) require date range extension or slot additions.',
                    'scheduled_count': partial_assigned,
                    'total_count': len(self.exam_subjects),
                    'steps': self.steps_taken,
                    'conflicts': conflicts_generated
                }

    def _backtrack(self, index, subjects, available_slots, assignment):
        if index >= len(subjects):
            return True

        if self.steps_taken >= self.max_steps:
            return False

        self.steps_taken += 1
        current = subjects[index]

        # Prioritize slot candidates that leave gaps for the same branch/semester
        slot_candidates = self._score_slots(current, available_slots, assignment)

        for date, slot in slot_candidates:
            if self._is_valid_assignment(current, date, slot, assignment):
                assignment[current.id] = (date, slot)
                if self._backtrack(index + 1, subjects, available_slots, assignment):
                    return True
                del assignment[current.id]

        return False

    def _is_valid_assignment(self, subject, date, slot, assignment):
        conflicting_ids = self.conflict_graph[subject.id]
        for assigned_id, (assigned_date, assigned_slot) in assignment.items():
            if assigned_date == date and assigned_slot.id == slot.id:
                # 1. Hard constraint: shared student clash
                if assigned_id in conflicting_ids:
                    return False
        return True

    def _score_slots(self, subject, available_slots, assignment):
        # Prefer earlier dates and maintain spacing
        scored = []
        for date, slot in available_slots:
            penalty = 0
            # Check gap with subjects in same semester/branch
            for assigned_id, (assigned_date, _) in assignment.items():
                assigned_es = next((s for s in self.exam_subjects if s.id == assigned_id), None)
                if assigned_es and assigned_es.subject.semester_id == subject.subject.semester_id:
                    if abs((date - assigned_date).days) == 0:
                        penalty += 10
                    elif abs((date - assigned_date).days) == 1:
                        penalty += 2
            scored.append((penalty, date, slot))

        scored.sort(key=lambda x: (x[0], x[1], x[2].start_time))
        return [(item[1], item[2]) for item in scored]
