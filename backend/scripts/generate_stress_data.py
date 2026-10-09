"""
ExamForge - High-Scale Institution Stress Testing & Benchmark Generator
Member 5: Performance Benchmarking & High-Concurrency Data Generation

Simulates large-scale institutional loads (500+ students, 20 examination halls,
multiple exam sessions) to benchmark constraint-solving algorithms and seating allocations.
"""

import os
import sys
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examforge.settings")

import django
django.setup()

from django.db import transaction
from apps.accounts.models import User
from apps.academics.models import Department, Branch, Semester, Subject
from apps.students.models import StudentProfile
from apps.infrastructure.models import ExaminationRoom, Building
from apps.registration.models import StudentEnrollment, SubjectRegistration

def generate_benchmark_dataset(num_students=200, num_rooms=10):
    print(f"[*] Commencing stress dataset generation ({num_students} students, {num_rooms} halls)...")

    dept = Department.objects.first()
    branch = Branch.objects.first()
    semester = Semester.objects.first()
    subjects = list(Subject.objects.filter(semester=semester))

    if not subjects:
        print("[!] No subjects found. Please seed basic data first.")
        return

    # 1. Create bulk test rooms
    bldg, _ = Building.objects.get_or_create(code="STRESS_BLDG", defaults={"name": "Engineering Annex", "total_floors": 4})
    for r_idx in range(1, num_rooms + 1):
        r_num = f"BENCH-{r_idx:02d}"
        ExaminationRoom.objects.get_or_create(
            room_number=r_num,
            defaults={
                "building": bldg,
                "floor": (r_idx % 4) + 1,
                "room_type": "HALL",
                "bench_capacity": 30,
                "rows": 6,
                "columns": 5,
                "usable_capacity": 30,
                "is_active": True,
                "has_cctv": True,
            }
        )

    # 2. Create bulk students
    created_count = 0
    with transaction.atomic():
        for i in range(1, num_students + 1):
            roll = f"STRESS-24CS{i:04d}"
            reg = f"REG-BENCH-{i:04d}"
            email = f"stress.student{i}@university.edu"

            u, _ = User.objects.get_or_create(
                username=roll.lower(),
                defaults={
                    "email": email,
                    "first_name": f"StressCandidate",
                    "last_name": f"#{i}",
                    "role": "STUDENT"
                }
            )
            u.set_password("stress123")
            u.save()

            sp, _ = StudentProfile.objects.get_or_create(
                user=u,
                defaults={
                    "registration_number": reg,
                    "roll_number": roll,
                    "department": dept,
                    "branch": branch,
                    "current_semester": semester,
                    "gender": "O",
                    "blood_group": "B+",
                    "admission_year": 2024,
                    "status": "ACTIVE"
                }
            )

            # Enroll student in semester
            enr, _ = StudentEnrollment.objects.get_or_create(
                student=sp,
                semester=semester,
                defaults={"academic_year": "2025-2026", "enrollment_status": "APPROVED"}
            )

            # Register in 3-4 subjects
            for sub in random.sample(subjects, min(len(subjects), 3)):
                att_pct = random.uniform(70.0, 95.0)
                SubjectRegistration.objects.get_or_create(
                    enrollment=enr,
                    subject=sub,
                    defaults={
                        "attendance_percentage": att_pct,
                        "is_eligible_for_exam": (att_pct >= 75.0),
                        "approval_status": "APPROVED"
                    }
                )

            created_count += 1

    print(f"[SUCCESS] High-scale benchmark fixtures generated successfully: {created_count} candidates enrolled.")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    generate_benchmark_dataset(num_students=count)
