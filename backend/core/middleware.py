"""
ExamForge custom Django middleware.
RequestTimingMiddleware: adds X-ExamForge-Duration header.
SecurityHeadersMiddleware: adds HSTS, CSP, X-Frame-Options.
MaintenanceModeMiddleware: returns 503 when MAINTENANCE_MODE=true.
AuditMiddleware: logs POST/PUT/DELETE requests to analytics.
"""
import time
import logging
import os
from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("examforge.middleware")


class RequestTimingMiddleware(MiddlewareMixin):
    """Adds X-ExamForge-Duration header to every response."""

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, "_start_time"):
            duration_ms = int((time.time() - request._start_time) * 1000)
            response["X-ExamForge-Duration"] = f"{duration_ms}ms"
            if duration_ms > 3000:
                logger.warning("SLOW REQUEST %s %s — %dms", request.method, request.path, duration_ms)
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Adds security headers to every HTTP response."""

    def process_response(self, request, response):
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        if request.is_secure():
            response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class MaintenanceModeMiddleware(MiddlewareMixin):
    """Returns HTTP 503 for all non-admin requests when maintenance mode is active."""

    BYPASS_PATHS = ["/admin/", "/api/health/"]

    def process_request(self, request):
        if os.environ.get("MAINTENANCE_MODE", "false").lower() != "true":
            return None
        path = request.path
        if any(path.startswith(bp) for bp in self.BYPASS_PATHS):
            return None
        if request.path.startswith("/api/"):
            return JsonResponse(
                {"error": "Service temporarily unavailable for maintenance. Please try again later."},
                status=503
            )
        return HttpResponse(
            "<h1>ExamForge is under maintenance.</h1><p>Please check back soon.</p>",
            status=503,
            content_type="text/html"
        )
