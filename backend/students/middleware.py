"""ExamForge M2 — Student Request Logging Middleware"""
import logging
import time

logger = logging.getLogger('students.middleware')

class StudentRequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = round((time.time() - start_time) * 1000, 2)

        if request.path.startswith('/api/v1/students/') or request.path.startswith('/api/v1/registrations/'):
            user_id = getattr(request.user, 'id', 'anonymous')
            logger.info(
                f"[M2 Request] {request.method} {request.path} | Status: {response.status_code} | "
                f"User: {user_id} | Time: {duration}ms"
            )
        return response
