"""
ExamForge validation utilities.
Shared validators for academic codes, roll numbers, email patterns,
date ranges, and capacity constraints used across multiple Django apps.
"""
import re
import logging
from datetime import date, datetime
from typing import Optional, Union

logger = logging.getLogger("examforge.core.validators")


class ValidationError(Exception):
    """Raised when ExamForge validation fails."""
    def __init__(self, message: str, field: Optional[str] = None, code: str = "invalid"):
        self.message = message
        self.field = field
        self.code = code
        super().__init__(message)


# ── Academic code validators ──────────────────────────────────────

DEPT_CODE_PATTERN = re.compile(r"^[A-Z]{2,6}$")
PROGRAM_CODE_PATTERN = re.compile(r"^[A-Z]{2,4}[0-9]{0,2}$")
COURSE_CODE_PATTERN = re.compile(r"^[A-Z]{2,4}[0-9]{3,4}$")
HALL_CODE_PATTERN = re.compile(r"^[A-Z]{1,4}-[0-9]{1,4}[A-Z]?$")


def validate_department_code(code: str) -> str:
    code = code.strip().upper()
    if not DEPT_CODE_PATTERN.match(code):
        raise ValidationError(
            f"'{code}' is not a valid department code. Expected 2-6 uppercase letters (e.g. 'CSE', 'ECE').",
            field="code",
            code="invalid_dept_code"
        )
    return code


def validate_program_code(code: str) -> str:
    code = code.strip().upper()
    if not PROGRAM_CODE_PATTERN.match(code):
        raise ValidationError(
            f"'{code}' is not a valid program code. Expected 2-4 uppercase letters optionally followed by digits.",
            field="code",
            code="invalid_program_code"
        )
    return code


def validate_course_code(code: str) -> str:
    code = code.strip().upper()
    if not COURSE_CODE_PATTERN.match(code):
        raise ValidationError(
            f"'{code}' is not a valid course code. Expected format like 'CS301' or 'ECE4101'.",
            field="code",
            code="invalid_course_code"
        )
    return code


def validate_hall_code(code: str) -> str:
    code = code.strip().upper()
    if not HALL_CODE_PATTERN.match(code):
        raise ValidationError(
            f"'{code}' is not a valid hall code. Expected format like 'AB-101' or 'LH-02A'.",
            field="code",
            code="invalid_hall_code"
        )
    return code


# ── Roll number validator ──────────────────────────────────────

ROLL_NUMBER_PATTERN = re.compile(
    r"^[0-9]{2}[A-Z]{2,4}[0-9]{4}$"  # e.g. 23CSE0042
)


def validate_roll_number(roll: str) -> str:
    roll = roll.strip().upper()
    if not ROLL_NUMBER_PATTERN.match(roll):
        raise ValidationError(
            f"'{roll}' is not a valid roll number. Expected format: 2-digit year + dept code + 4-digit serial (e.g. 23CSE0042).",
            field="roll_number",
            code="invalid_roll_number"
        )
    return roll


def validate_roll_number_batch(roll_numbers: list[str]) -> dict:
    """
    Validate a batch of roll numbers.
    Returns: {"valid": [...], "invalid": [{"roll": ..., "error": ...}]}
    """
    valid, invalid = [], []
    for roll in roll_numbers:
        try:
            valid.append(validate_roll_number(roll))
        except ValidationError as e:
            invalid.append({"roll": roll, "error": e.message})
    return {"valid": valid, "invalid": invalid, "total": len(roll_numbers)}


# ── Email validators ──────────────────────────────────────

INSTITUTIONAL_EMAIL_DOMAINS = [
    "examforge.edu", "institution.ac.in", "college.edu.in",
]


def validate_institutional_email(email: str, allowed_domains: Optional[list] = None) -> str:
    email = email.strip().lower()
    if "@" not in email:
        raise ValidationError(f"'{email}' is not a valid email address.", field="email")
    domain = email.split("@")[1]
    domains = allowed_domains or INSTITUTIONAL_EMAIL_DOMAINS
    # For flexibility, we just check it's a properly formatted email
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
    if not email_pattern.match(email):
        raise ValidationError(f"'{email}' is not a valid email format.", field="email")
    return email


# ── Date range validators ──────────────────────────────────────

def validate_date_range(start: date, end: date, field_prefix: str = "") -> None:
    if start > end:
        prefix = f"{field_prefix}_" if field_prefix else ""
        raise ValidationError(
            f"Start date ({start}) must not be after end date ({end}).",
            field=f"{prefix}start_date",
            code="invalid_date_range"
        )


def validate_future_date(d: date, field: str = "date", allow_today: bool = True) -> date:
    today = date.today()
    if allow_today and d < today:
        raise ValidationError(
            f"Date must be today or in the future. Got: {d}.",
            field=field,
            code="past_date"
        )
    elif not allow_today and d <= today:
        raise ValidationError(
            f"Date must be strictly in the future. Got: {d}.",
            field=field,
            code="past_or_today_date"
        )
    return d


def validate_exam_session_dates(
    start: date,
    end: date,
    registration_deadline: Optional[date] = None,
) -> None:
    validate_date_range(start, end, "exam_session")
    if registration_deadline:
        if registration_deadline >= start:
            raise ValidationError(
                f"Registration deadline ({registration_deadline}) must be before exam start ({start}).",
                field="registration_deadline",
                code="invalid_deadline"
            )


# ── Capacity validators ──────────────────────────────────────

def validate_hall_capacity(rows: int, columns: int, usable_pct: float = 0.8) -> dict:
    if rows <= 0 or columns <= 0:
        raise ValidationError("Hall rows and columns must be positive integers.")
    if not (0.1 <= usable_pct <= 1.0):
        raise ValidationError("Usable percentage must be between 0.1 and 1.0.")
    total = rows * columns
    usable = int(total * usable_pct)
    return {
        "rows": rows,
        "columns": columns,
        "total_desks": total,
        "usable_capacity": usable,
        "reserved": total - usable,
    }


def validate_invigilation_ratio(student_count: int, faculty_count: int, min_ratio: int = 20) -> None:
    if faculty_count <= 0:
        raise ValidationError("At least one faculty member must be assigned for invigilation.")
    ratio = student_count / faculty_count
    if ratio > min_ratio:
        raise ValidationError(
            f"Invigilation ratio {ratio:.1f}:1 exceeds maximum of {min_ratio}:1. "
            f"Need at least {int(student_count / min_ratio) + 1} faculty for {student_count} students.",
            field="faculty_count",
            code="insufficient_invigilators"
        )


# ── CSV import validators ──────────────────────────────────────

REQUIRED_STUDENT_CSV_COLUMNS = {
    "roll_number", "full_name", "email", "department_code",
    "program_code", "semester", "academic_year",
}


def validate_student_csv_headers(headers: list[str]) -> dict:
    header_set = {h.strip().lower() for h in headers}
    missing = REQUIRED_STUDENT_CSV_COLUMNS - header_set
    extra = header_set - REQUIRED_STUDENT_CSV_COLUMNS
    return {
        "valid": len(missing) == 0,
        "missing_columns": sorted(missing),
        "extra_columns": sorted(extra),
        "provided_columns": sorted(header_set),
    }


def validate_student_csv_row(row: dict, row_index: int) -> dict:
    errors = []
    warnings = []

    roll = row.get("roll_number", "").strip()
    if not roll:
        errors.append({"field": "roll_number", "error": "Roll number is required."})
    else:
        try:
            validate_roll_number(roll)
        except ValidationError as e:
            errors.append({"field": "roll_number", "error": e.message})

    email = row.get("email", "").strip()
    if not email:
        errors.append({"field": "email", "error": "Email is required."})
    else:
        try:
            validate_institutional_email(email)
        except ValidationError as e:
            warnings.append({"field": "email", "warning": e.message})

    dept = row.get("department_code", "").strip()
    if dept:
        try:
            validate_department_code(dept)
        except ValidationError as e:
            errors.append({"field": "department_code", "error": e.message})

    semester_str = row.get("semester", "").strip()
    try:
        semester = int(semester_str)
        if not (1 <= semester <= 8):
            errors.append({"field": "semester", "error": f"Semester must be 1-8, got {semester}."})
    except ValueError:
        errors.append({"field": "semester", "error": f"Semester must be a number, got '{semester_str}'."})

    return {
        "row": row_index,
        "is_valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }
