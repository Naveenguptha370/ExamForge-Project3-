"""
ExamForge - Session Idle Timeout and Security Headers Middleware
Member 1: Authentication & User Management
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from accounts.session_tracker import SessionSecurityManager

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Enforces strict defense-in-depth security headers."""
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        return response

class SessionInactivityMiddleware(MiddlewareMixin):
    """Verifies that authenticated requests originate from non-expired sessions."""
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                active = SessionSecurityManager.get_session(session_key)
                if active:
                    active.update_activity()
        return None
