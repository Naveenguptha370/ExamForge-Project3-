"""
ExamForge - Audit Trail & Security Diff Service
Member 1: Authentication & User Management
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from accounts.models import AuditLog, User

class AuditTrailService:
    """
    Captures tamper-evident audit logs across accounts and faculty subsystems.
    Generates JSON delta diffs between previous and new model states.
    """

    @staticmethod
    def calculate_diff(old_state: Dict[str, Any], new_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        diff = {}
        all_keys = set(old_state.keys()).union(set(new_state.keys()))
        for key in all_keys:
            if key in ('password', '_state', 'created_at', 'updated_at'):
                continue
            old_val = old_state.get(key)
            new_val = new_state.get(key)
            if old_val != new_val:
                diff[key] = {
                    'before': str(old_val),
                    'after': str(new_val)
                }
        return diff

    @classmethod
    def log_event(
        cls,
        actor: Optional[User],
        action: str,
        model_name: str,
        object_id: str,
        details: str = "",
        diff: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        payload = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'message': details,
            'delta': diff or {}
        }
        return AuditLog.objects.create(
            actor=actor,
            action=action,
            model_name=model_name,
            object_id=object_id,
            details=json.dumps(payload),
            ip_address=ip_address
        )

    @classmethod
    def get_user_history(cls, user_id: int):
        return AuditLog.objects.filter(model_name='User', object_id=str(user_id)).order_by('-created_at')

    @classmethod
    def get_faculty_history(cls, faculty_id: str):
        return AuditLog.objects.filter(model_name='FacultyProfile', object_id=str(faculty_id)).order_by('-created_at')
