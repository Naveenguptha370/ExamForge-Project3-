"""
ExamForge - User Lifecycle & Status Transition Manager
Member 1: Authentication & User Management
"""
from typing import Dict, List

class UserLifecycleState:
    PENDING_ACTIVATION = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"
    ARCHIVED = "ARCHIVED"

class UserLifecycleManager:
    _VALID_TRANSITIONS: Dict[str, List[str]] = {
        UserLifecycleState.PENDING_ACTIVATION: [UserLifecycleState.ACTIVE, UserLifecycleState.INACTIVE],
        UserLifecycleState.ACTIVE: [UserLifecycleState.SUSPENDED, UserLifecycleState.INACTIVE, UserLifecycleState.ARCHIVED],
        UserLifecycleState.SUSPENDED: [UserLifecycleState.ACTIVE, UserLifecycleState.INACTIVE, UserLifecycleState.ARCHIVED],
        UserLifecycleState.INACTIVE: [UserLifecycleState.ACTIVE, UserLifecycleState.ARCHIVED],
        UserLifecycleState.ARCHIVED: []
    }

    @classmethod
    def can_transition(cls, current_status: str, target_status: str) -> bool:
        return target_status in cls._VALID_TRANSITIONS.get(current_status, [])
