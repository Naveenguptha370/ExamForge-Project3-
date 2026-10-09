"""
ExamForge - User Lifecycle & Status Transition Manager
Member 1: Authentication & User Management
"""
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime, timezone
from accounts.models import User, AuditLog

class UserLifecycleState:
    PENDING_ACTIVATION = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"

class UserLifecycleManager:
    """
    Governs user account lifecycle transitions, approvals, suspension, and safe archival.
    Ensures state transitions follow institutional policy and are fully auditable.
    """
    _VALID_TRANSITIONS: Dict[str, List[str]] = {
        UserLifecycleState.PENDING_ACTIVATION: [UserLifecycleState.ACTIVE, UserLifecycleState.INACTIVE],
        UserLifecycleState.ACTIVE: [UserLifecycleState.SUSPENDED, UserLifecycleState.INACTIVE, UserLifecycleState.ARCHIVED],
        UserLifecycleState.SUSPENDED: [UserLifecycleState.ACTIVE, UserLifecycleState.INACTIVE, UserLifecycleState.ARCHIVED],
        UserLifecycleState.INACTIVE: [UserLifecycleState.ACTIVE, UserLifecycleState.ARCHIVED],
        UserLifecycleState.ARCHIVED: []  # Terminal state
    }

    @classmethod
    def can_transition(cls, current_status: str, target_status: str) -> bool:
        allowed = cls._VALID_TRANSITIONS.get(current_status, [])
        return target_status in allowed

    @classmethod
    def transition_user(
        cls,
        user: User,
        target_status: str,
        actor: Optional[User],
        reason: str,
        ip_address: Optional[str] = None
    ) -> Tuple[bool, str]:
        if user.is_admin and target_status in (UserLifecycleState.INACTIVE, UserLifecycleState.SUSPENDED):
            if actor and actor.pk == user.pk:
                return (False, "Administrators cannot deactivate or suspend their own account.")

        if not cls.can_transition(user.status, target_status):
            return (False, f"Transition from '{user.status}' to '{target_status}' is disallowed.")

        old_status = user.status
        user.status = target_status
        user.is_active = (target_status == UserLifecycleState.ACTIVE)
        user.save(update_fields=['status', 'is_active'])

        # Audit event
        AuditLog.objects.create(
            actor=actor,
            action=f"USER_STATUS_{target_status}",
            model_name="User",
            object_id=str(user.pk),
            details=f"Status changed from {old_status} to {target_status}. Reason: {reason}",
            ip_address=ip_address
        )
        return (True, f"User status successfully transitioned to {target_status}.")

    @classmethod
    def bulk_deactivate_users(
        cls,
        user_ids: List[int],
        actor: User,
        reason: str,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        results = {'success': [], 'failed': []}
        for uid in user_ids:
            try:
                user = User.objects.get(pk=uid)
                ok, msg = cls.transition_user(user, UserLifecycleState.INACTIVE, actor, reason, ip_address)
                if ok:
                    results['success'].append(uid)
                else:
                    results['failed'].append({'id': uid, 'error': msg})
            except User.DoesNotExist:
                results['failed'].append({'id': uid, 'error': 'User not found'})
        return results
