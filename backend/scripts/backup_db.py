"""
ExamForge - Automated Institutional Database Backup Script
Member 5: Audit, Settings & Disaster Recovery Subsystem

Usage:
    python backend/scripts/backup_db.py [--format json|sql] [--output-dir /path/to/backups]
"""

import os
import sys
import shutil
import datetime
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examforge.settings")

import django
django.setup()

from django.core.management import call_command
from django.conf import settings
from apps.audit.models import AuditLog
from apps.accounts.models import User

def perform_system_backup(output_dir=None):
    if not output_dir:
        output_dir = BASE_DIR / "backups"
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(output_dir, f"examforge_backup_{timestamp}.json")

    print(f"[*] Starting ExamForge full-database snapshot...")
    print(f"[*] Target backup file: {backup_file}")

    with open(backup_file, "w", encoding="utf-8") as f:
        call_command(
            "dumpdata",
            "--natural-foreign",
            "--natural-primary",
            "--indent", "2",
            "--exclude", "contenttypes",
            "--exclude", "auth.permission",
            stdout=f
        )

    file_size_kb = os.path.getsize(backup_file) / 1024
    print(f"[SUCCESS] Database backup completed: {file_size_kb:.2f} KB written.")

    # Record in AuditLog
    admin_user = User.objects.filter(role="ADMIN").first()
    AuditLog.log_event(
        user=admin_user,
        action="EXPORT",
        category="SETTINGS",
        entity_name="DatabaseBackup",
        entity_id=timestamp,
        details={"backup_file": str(backup_file), "size_kb": file_size_kb},
        ip_address="127.0.0.1"
    )

    return backup_file

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    perform_system_backup(out)
