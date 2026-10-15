"""
ExamForge utility functions.
Miscellaneous helpers used across the project for PDF generation setup,
file handling, date math, code generation, and environment utilities.
"""
import os
import re
import uuid
import hashlib
import logging
import secrets
import string
from datetime import date, datetime, timedelta
from typing import Optional, Union, Generator
from pathlib import Path

logger = logging.getLogger("examforge.core.utils")


# ── Code & identifier generation ──────────────────────────────────────

def generate_roll_number(dept_code: str, year: int, sequence: int) -> str:
    """
    Generate a standardized student roll number.
    Format: {2-digit-year}{DEPT}{4-digit-seq}
    e.g. 23CSE0042
    """
    year_suffix = str(year)[-2:]
    dept = dept_code.strip().upper()[:4]
    seq = str(sequence).zfill(4)
    return f"{year_suffix}{dept}{seq}"


def generate_registration_code(session_code: str, student_roll: str) -> str:
    """Generate a unique registration reference code."""
    unique_part = uuid.uuid4().hex[:6].upper()
    return f"REG-{session_code}-{student_roll}-{unique_part}"


def generate_hall_ticket_number(session_code: str, roll_number: str) -> str:
    """Generate a tamper-evident hall ticket number using HMAC-style hashing."""
    raw = f"{session_code}:{roll_number}:{secrets.token_hex(4)}"
    digest = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"HT-{session_code[:4]}-{digest}"


def generate_exam_session_code(year: int, season: str, suffix: str = "") -> str:
    """
    Generate standard exam session code.
    e.g. generate_exam_session_code(2026, "ODD") -> "2026-ODD"
         generate_exam_session_code(2026, "EVEN", "MID") -> "2026-EVEN-MID"
    """
    parts = [str(year), season.strip().upper()]
    if suffix:
        parts.append(suffix.strip().upper())
    return "-".join(parts)


def generate_temp_password(length: int = 12) -> str:
    """Generate a secure temporary password meeting standard complexity requirements."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        pwd = "".join(secrets.choice(chars) for _ in range(length))
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in "!@#$%^&*" for c in pwd)
        if has_upper and has_lower and has_digit and has_special:
            return pwd


# ── Date and time utilities ──────────────────────────────────────

def get_academic_year(reference_date: Optional[date] = None) -> str:
    """
    Determine current academic year string.
    Academic years run July -> June.
    e.g. For Oct 2026 -> "2026-27"
    """
    d = reference_date or date.today()
    if d.month >= 7:
        return f"{d.year}-{str(d.year + 1)[-2:]}"
    return f"{d.year - 1}-{str(d.year)[-2:]}"


def get_semester_season(reference_date: Optional[date] = None) -> str:
    """
    Return "ODD" (July-Nov) or "EVEN" (Jan-May) based on current month.
    """
    d = reference_date or date.today()
    return "ODD" if d.month in range(7, 12) else "EVEN"


def working_days_between(start: date, end: date, exclude_sundays: bool = True) -> int:
    """Count working days between two dates (excluding Sundays by default)."""
    total = 0
    current = start
    while current <= end:
        if not (exclude_sundays and current.weekday() == 6):
            total += 1
        current += timedelta(days=1)
    return total


def format_duration(seconds: int) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        mins, secs = divmod(seconds, 60)
        return f"{mins}m {secs}s"
    elif seconds < 86400:
        hours, rem = divmod(seconds, 3600)
        mins = rem // 60
        return f"{hours}h {mins}m"
    else:
        days, rem = divmod(seconds, 86400)
        hours = rem // 3600
        return f"{days}d {hours}h"


# ── File handling utilities ──────────────────────────────────────

def safe_filename(name: str) -> str:
    """Convert arbitrary string to a safe filename."""
    name = re.sub(r"[^\w\s\-\.]", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:200]


def get_upload_path(instance, filename: str) -> str:
    """Generate a structured upload path for Django FileField/ImageField."""
    model_name = instance.__class__.__name__.lower()
    today = date.today()
    ext = Path(filename).suffix.lower()
    unique = uuid.uuid4().hex[:8]
    safe = safe_filename(Path(filename).stem)
    return f"uploads/{model_name}/{today.year}/{today.month:02d}/{safe}_{unique}{ext}"


def read_csv_chunks(filepath: str, chunk_size: int = 500) -> Generator[list, None, None]:
    """Read a CSV file in chunks for memory-efficient batch processing."""
    import csv
    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        chunk = []
        for row in reader:
            chunk.append(dict(row))
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


# ── Environment utilities ──────────────────────────────────────

def get_required_env(key: str) -> str:
    """Get an environment variable or raise with a clear error message."""
    value = os.environ.get(key)
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            "Check your .env file or deployment environment configuration."
        )
    return value


def is_production() -> bool:
    return os.environ.get("DJANGO_ENV", "development").lower() == "production"


def is_development() -> bool:
    return not is_production()


# ── Pagination utilities ──────────────────────────────────────

def paginate_queryset(queryset, page: int = 1, page_size: int = 25):
    """
    Simple manual pagination for non-DRF contexts (management commands, reports).
    Returns: (page_items, total_count, total_pages, has_more)
    """
    from django.core.paginator import Paginator, EmptyPage, InvalidPage
    paginator = Paginator(queryset, page_size)
    total_count = paginator.count
    total_pages = paginator.num_pages
    try:
        page_obj = paginator.page(page)
        items = list(page_obj.object_list)
        has_more = page_obj.has_next()
    except (EmptyPage, InvalidPage):
        items, has_more = [], False
    return items, total_count, total_pages, has_more


# ── Text utilities ──────────────────────────────────────

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)].rstrip() + suffix


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s\-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def pluralize(count: int, singular: str, plural: Optional[str] = None) -> str:
    if count == 1:
        return f"{count} {singular}"
    return f"{count} {plural or singular + 's'}"
