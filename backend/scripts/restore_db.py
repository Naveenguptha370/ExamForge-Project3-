"""
ExamForge - Automated Institutional Database Restore Script
Member 5: Audit, Settings & Disaster Recovery Subsystem

Usage:
    python backend/scripts/restore_db.py <path_to_backup_file.json>
"""

import os
import sys
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examforge.settings")

import django
django.setup()

from django.core.management import call_command
from apps.audit.models import AuditLog
from apps.accounts.models import User

def restore_system_backup(backup_file):
    if not os.path.exists(backup_file):
        print(f"[ERROR] Backup file '{backup_file}' does not exist.")
        sys.exit(1)

    print(f"[*] Restoring ExamForge database from: {backup_file}")
    
    call_command("loaddata", backup_file)
    print(f"[SUCCESS] Database successfully restored from {backup_file}.")

    admin_user = User.objects.filter(role="ADMIN").first()
    AuditLog.log_event(
        user=admin_user,
        action="UPDATE",
        category="SETTINGS",
        entity_name="DatabaseRestore",
        entity_id=os.path.basename(backup_file),
        details={"restored_from": str(backup_file)},
        ip_address="127.0.0.1"
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backend/scripts/restore_db.py <backup_file.json>")
        sys.exit(1)
    restore_system_backup(sys.argv[1])
