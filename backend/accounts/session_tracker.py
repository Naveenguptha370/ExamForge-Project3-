"""
ExamForge - Session Security & Device Tracking
Member 1: Authentication & User Management
"""
import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta

class UserDeviceSession:
    def __init__(self, session_key: str, user_id: int, user_agent: str, ip_address: str):
        self.session_key = session_key
        self.user_id = user_id
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.created_at = datetime.now(timezone.utc)
        self.last_activity = datetime.now(timezone.utc)

    def update_activity(self):
        self.last_activity = datetime.now(timezone.utc)

class SessionSecurityManager:
    MAX_CONCURRENT_SESSIONS = 3
    IDLE_TIMEOUT_MINUTES = 30
    _active_sessions: Dict[str, UserDeviceSession] = {}

    @classmethod
    def register_session(cls, user_id: int, user_agent: str, ip_address: str) -> UserDeviceSession:
        user_sessions = [s for s in cls._active_sessions.values() if s.user_id == user_id]
        if len(user_sessions) >= cls.MAX_CONCURRENT_SESSIONS:
            user_sessions.sort(key=lambda s: s.last_activity)
            cls.terminate_session(user_sessions[0].session_key)

        session_key = str(uuid.uuid4())
        session = UserDeviceSession(session_key, user_id, user_agent, ip_address)
        cls._active_sessions[session_key] = session
        return session

    @classmethod
    def terminate_session(cls, session_key: str) -> bool:
        if session_key in cls._active_sessions:
            del cls._active_sessions[session_key]
            return True
        return False

    @classmethod
    def get_user_sessions(cls, user_id: int) -> List[UserDeviceSession]:
        return [s for s in cls._active_sessions.values() if s.user_id == user_id]
