"""
ExamForge - Bulk User & Faculty Import/Export Engine
Member 1: Authentication, User Management, and Faculty Management
"""
import csv
import io
import re
from typing import Dict, Any, List, Tuple

class BulkFacultyImportParser:
    """Parses, validates, and stages bulk CSV rosters of faculty accounts."""
    REQUIRED_FIELDS = ['faculty_id', 'username', 'email', 'department', 'designation']

    @classmethod
    def parse_csv(cls, csv_text: str) -> Dict[str, Any]:
        reader = csv.DictReader(io.StringIO(csv_text.strip()))
        valid_rows = []
        invalid_rows = []

        for idx, row in enumerate(reader, start=1):
            errors = []
            for rf in cls.REQUIRED_FIELDS:
                if not row.get(rf) or not row[rf].strip():
                    errors.append(f"Missing required field: '{rf}'")

            email = row.get('email', '').strip()
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append(f"Invalid email format: '{email}'")

            if errors:
                invalid_rows.append({'row_number': idx, 'data': row, 'errors': errors})
            else:
                valid_rows.append({'row_number': idx, 'data': row})

        return {
            'total_rows': len(valid_rows) + len(invalid_rows),
            'valid_count': len(valid_rows),
            'invalid_count': len(invalid_rows),
            'valid_rows': valid_rows,
            'invalid_rows': invalid_rows
        }
