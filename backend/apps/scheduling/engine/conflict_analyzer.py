import datetime
from collections import defaultdict
from apps.scheduling.models import SchedulingClash, ClashType, ClashSeverity
from apps.students.models import SubjectRegistration, EligibilityStatus
from apps.infrastructure.models import Room
from apps.academics.models import Subject

class ConflictAnalyzer:
    """
    Examines scheduled timetable entries against institutional hard & soft constraints.
    Produces detailed clash reports with student names, conflict reasons, and fix suggestions.
    """

    def __init__(self, timetable):
        self.timetable = timetable
        self.session = timetable.session
        self.constraints = getattr(self.session, 'constraint_config', None)

    def analyze(self):
        """
        Runs full conflict audit across all entries in the timetable.
        Clears previous clashes and creates new SchedulingClash records.
        Returns a dictionary with summary metrics and lists of detected clashes.
        """
        # Remove previous clashes
        self.timetable.clashes.all().delete()

        entries = list(self.timetable.entries.select_related(
            'subject_config__subject',
            'subject_config__subject__department',
            'subject_config__subject__branch',
            'time_slot'
        ).all())

        if not entries:
            return {
                'is_conflict_free': True,
                'clash_count': 0,
                'critical_count': 0,
                'high_count': 0,
                'medium_count': 0,
                'clashes': []
            }

        clashes_created = []

        # 1. Index entries by (date, slot)
        slot_map = defaultdict(list)
        # 2. Index entries by date
        date_map = defaultdict(list)
        # 3. Index entries by branch + semester
        branch_sem_entries = defaultdict(list)

        for entry in entries:
            slot_key = (entry.exam_date, entry.time_slot_id)
            slot_map[slot_key].append(entry)
            date_map[entry.exam_date].append(entry)
            
            subj = entry.subject_config.subject
            if subj.branch_id:
                branch_sem_key = (subj.branch_id, subj.semester_number)
                branch_sem_entries[branch_sem_key].append(entry)

        # -------------------------------------------------------------
        # HARD CONSTRAINT 1: Same Slot Student Double Booking
        # -------------------------------------------------------------
        for (exam_date, slot_id), slot_entries in slot_map.items():
            if len(slot_entries) < 2:
                continue

            time_slot = slot_entries[0].time_slot

            for i in range(len(slot_entries)):
                for j in range(i + 1, len(slot_entries)):
                    entry_a = slot_entries[i]
                    entry_b = slot_entries[j]
                    subj_a = entry_a.subject_config.subject
                    subj_b = entry_b.subject_config.subject

                    # Check same branch + semester
                    if (subj_a.branch_id and subj_b.branch_id and 
                        subj_a.branch_id == subj_b.branch_id and 
                        subj_a.semester_number == subj_b.semester_number):
                        
                        desc = (
                            f"Branch & Semester Collision: Both '{subj_a.code} ({subj_a.name})' and "
                            f"'{subj_b.code} ({subj_b.name})' belong to {subj_a.branch.name} Sem {subj_a.semester_number} "
                            f"and are scheduled simultaneously on {exam_date} in {time_slot.name}."
                        )
                        clash = SchedulingClash.objects.create(
                            timetable=self.timetable,
                            clash_type=ClashType.BRANCH_SEM_OVERLAP,
                            severity=ClashSeverity.CRITICAL,
                            subject_1=subj_a,
                            subject_2=subj_b,
                            exam_date=exam_date,
                            time_slot=time_slot,
                            description=desc,
                            affected_students_count=entry_a.expected_students,
                            suggested_resolution=f"Reschedule '{subj_b.code}' to a different exam date or shift slot."
                        )
                        clashes_created.append(clash)
                        entry_a.has_conflict = True
                        entry_a.conflict_details = "Branch/Semester Slot Collision"
                        entry_b.has_conflict = True
                        entry_b.conflict_details = "Branch/Semester Slot Collision"
                        continue

                    # Check student registration overlap in DB
                    regs_a = set(SubjectRegistration.objects.filter(
                        subject=subj_a,
                        eligibility_status=EligibilityStatus.ELIGIBLE
                    ).values_list('student_id', 'student__register_number', 'student__first_name', 'student__last_name'))

                    student_ids_a = {r[0] for r in regs_a}
                    regs_b = SubjectRegistration.objects.filter(
                        subject=subj_b,
                        student_id__in=student_ids_a,
                        eligibility_status=EligibilityStatus.ELIGIBLE
                    ).select_related('student')

                    clashing_students = list(regs_b)
                    if clashing_students:
                        names = [f"{s.student.register_number} - {s.student.full_name}" for s in clashing_students[:10]]
                        desc = (
                            f"Student Double-Booking: {len(clashing_students)} students are registered for both "
                            f"'{subj_a.code}' and '{subj_b.code}' at the exact same slot ({exam_date}, {time_slot.name}). "
                            f"Affected students: {', '.join(names[:3])}{'...' if len(names) > 3 else ''}."
                        )
                        clash = SchedulingClash.objects.create(
                            timetable=self.timetable,
                            clash_type=ClashType.STUDENT_OVERLAP,
                            severity=ClashSeverity.CRITICAL,
                            subject_1=subj_a,
                            subject_2=subj_b,
                            exam_date=exam_date,
                            time_slot=time_slot,
                            description=desc,
                            affected_students_count=len(clashing_students),
                            affected_student_names=names,
                            suggested_resolution=f"Move '{subj_b.code}' to another date where enrolled students have no scheduled examinations."
                        )
                        clashes_created.append(clash)
                        entry_a.has_conflict = True
                        entry_a.conflict_details = "Student Double Booking Clash"
                        entry_b.has_conflict = True
                        entry_b.conflict_details = "Student Double Booking Clash"

        # -------------------------------------------------------------
        # HARD CONSTRAINT 2: Total Concurrent Usable Room Capacity
        # -------------------------------------------------------------
        total_campus_capacity = sum(
            Room.objects.filter(is_active=True).values_list('usable_exam_capacity', flat=True)
        ) or 600

        for (exam_date, slot_id), slot_entries in slot_map.items():
            slot_demand = sum(e.expected_students for e in slot_entries)
            if slot_demand > total_campus_capacity:
                first_entry = slot_entries[0]
                desc = (
                    f"Room Capacity Deficit: {slot_demand} students scheduled simultaneously on {exam_date} "
                    f"[{first_entry.time_slot.name}], exceeding total active institutional capacity ({total_campus_capacity} seats)."
                )
                clash = SchedulingClash.objects.create(
                    timetable=self.timetable,
                    clash_type=ClashType.ROOM_CAPACITY_DEFICIT,
                    severity=ClashSeverity.HIGH,
                    subject_1=first_entry.subject_config.subject,
                    exam_date=exam_date,
                    time_slot=first_entry.time_slot,
                    description=desc,
                    affected_students_count=slot_demand - total_campus_capacity,
                    suggested_resolution="Shift one or more examination subjects to an afternoon or evening shift slot."
                )
                clashes_created.append(clash)

        # -------------------------------------------------------------
        # SOFT CONSTRAINT 1: Study Gap Violations for Same Branch/Sem
        # -------------------------------------------------------------
        min_gap_hard = self.constraints.min_study_gap_days_hard if self.constraints else 1

        for (branch_id, sem_num), b_entries in branch_sem_entries.items():
            sorted_entries = sorted(b_entries, key=lambda x: x.exam_date)
            for k in range(len(sorted_entries) - 1):
                cur = sorted_entries[k]
                nxt = sorted_entries[k + 1]
                delta_days = (nxt.exam_date - cur.exam_date).days

                is_hard_subj = (
                    cur.subject_config.subject.difficulty == 'HARD' or 
                    nxt.subject_config.subject.difficulty == 'HARD'
                )

                if delta_days == 0:
                    # Same day multiple exams for same branch
                    desc = (
                        f"Same-Day Load: Students of {cur.subject.branch.name} Sem {sem_num} have 2 exams "
                        f"on the same day ({cur.exam_date}): '{cur.subject.code}' and '{nxt.subject.code}'."
                    )
                    clash = SchedulingClash.objects.create(
                        timetable=self.timetable,
                        clash_type=ClashType.STUDY_GAP_VIOLATION,
                        severity=ClashSeverity.HIGH,
                        subject_1=cur.subject,
                        subject_2=nxt.subject,
                        exam_date=cur.exam_date,
                        description=desc,
                        affected_students_count=cur.expected_students,
                        suggested_resolution=f"Provide at least 1 day gap between '{cur.subject.code}' and '{nxt.subject.code}'."
                    )
                    clashes_created.append(clash)

                elif is_hard_subj and delta_days < (min_gap_hard + 1):
                    # Hard subject without requested study gap
                    desc = (
                        f"Insufficient Study Gap: Difficult subject '{cur.subject.code} ({cur.subject.name})' has only "
                        f"{delta_days - 1} rest days before '{nxt.subject.code}'. Recommended study gap: {min_gap_hard} day(s)."
                    )
                    clash = SchedulingClash.objects.create(
                        timetable=self.timetable,
                        clash_type=ClashType.CONSECUTIVE_DIFFICULT,
                        severity=ClashSeverity.MEDIUM,
                        subject_1=cur.subject,
                        subject_2=nxt.subject,
                        exam_date=cur.exam_date,
                        description=desc,
                        affected_students_count=cur.expected_students,
                        suggested_resolution="Insert an additional non-exam day or easier subject in between."
                    )
                    clashes_created.append(clash)

        # Save updated flags on entries
        for entry in entries:
            entry.save()

        critical_count = sum(1 for c in clashes_created if c.severity == ClashSeverity.CRITICAL)
        high_count = sum(1 for c in clashes_created if c.severity == ClashSeverity.HIGH)
        medium_count = sum(1 for c in clashes_created if c.severity == ClashSeverity.MEDIUM)

        is_free = (critical_count == 0)

        self.timetable.is_conflict_free = is_free
        self.timetable.clash_count = len(clashes_created)
        if is_free:
            if self.timetable.status == 'DRAFT':
                self.timetable.status = 'VALIDATED'
        else:
            self.timetable.status = 'DRAFT'
        self.timetable.save()

        return {
            'is_conflict_free': is_free,
            'clash_count': len(clashes_created),
            'critical_count': critical_count,
            'high_count': high_count,
            'medium_count': medium_count,
            'clashes': clashes_created
        }
