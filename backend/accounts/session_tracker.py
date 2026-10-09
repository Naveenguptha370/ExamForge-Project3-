"""
ExamForge - Session Security & Device Tracking
Member 1: Authentication & User Management
"""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta

class UserDeviceSession:
    """Represents an active authenticated device session."""
    def __init__(self, session_key: str, user_id: int, user_agent: str, ip_address: str):
        self.session_key = session_key
        self.user_id = user_id
        self.user_agent = user_agent
        self.ip_address = ip_address
        self.created_at = datetime.now(timezone.utc)
        self.last_activity = datetime.now(timezone.utc)
        self.device_type = self._parse_device_type(user_agent)

    def _parse_device_type(self, ua: str) -> str:
        ua_lower = ua.lower()
        if 'mobile' in ua_lower or 'android' in ua_lower or 'iphone' in ua_lower:
            return 'MOBILE'
        if 'tablet' in ua_lower or 'ipad' in ua_lower:
            return 'TABLET'
        return 'DESKTOP'

    def update_activity(self):
        self.last_activity = datetime.now(timezone.utc)

class SessionSecurityManager:
    """
    Tracks and limits concurrent sessions per user.
    Terminates inactive sessions exceeding idle timeout.
    """
    MAX_CONCURRENT_SESSIONS = 3
    IDLE_TIMEOUT_MINUTES = 30

    _active_sessions: Dict[str, UserDeviceSession] = {}

    @classmethod
    def register_session(cls, user_id: int, user_agent: str, ip_address: str) -> UserDeviceSession:
        user_sessions = [s for s in cls._active_sessions.values() if s.user_id == user_id]
        if len(user_sessions) >= cls.MAX_CONCURRENT_SESSIONS:
            user_sessions.sort(key=lambda s: s.last_activity)
            oldest = user_sessions[0]
            cls.terminate_session(oldest.session_key)

        session_key = str(uuid.uuid4())
        session = UserDeviceSession(session_key, user_id, user_agent, ip_address)
        cls._active_sessions[session_key] = session
        return session

    @classmethod
    def get_session(cls, session_key: str) -> Optional[UserDeviceSession]:
        session = cls._active_sessions.get(session_key)
        if not session:
            return None
        now = datetime.now(timezone.utc)
        if now - session.last_activity > timedelta(minutes=cls.IDLE_TIMEOUT_MINUTES):
            cls.terminate_session(session_key)
            return None
        session.update_activity()
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
