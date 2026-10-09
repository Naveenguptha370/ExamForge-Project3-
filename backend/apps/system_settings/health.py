"""
ExamForge - System Health & Operational Status Subsystem
Member 5: Health Monitoring & Production Observability
"""

import os
import time
from django.db import connection
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from apps.examinations.models import ExamSession
from apps.halltickets.models import HallTicket
from apps.scheduling.models import Timetable

class SystemHealthView(APIView):
    """
    Health check and infrastructure telemetry endpoint.
    Permits unauthenticated ping for container healthchecks,
    while returning comprehensive diagnostics.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        start_time = time.time()
        diagnostics = {
            "status": "HEALTHY",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "system": "ExamForge Examination Operations System",
            "version": "1.0.0",
            "checks": {}
        }

        # 1. Database Connectivity Check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
                db_healthy = (row[0] == 1)
            diagnostics["checks"]["database"] = {
                "status": "PASS",
                "vendor": connection.vendor,
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }
        except Exception as e:
            diagnostics["status"] = "DEGRADED"
            diagnostics["checks"]["database"] = {
                "status": "FAIL",
                "error": str(e)
            }

        # 2. Local Media Storage Check (ReportLab PDFs & Backups)
        media_path = str(settings.MEDIA_ROOT)
        media_writable = os.access(media_path, os.W_OK) if os.path.exists(media_path) else False
        diagnostics["checks"]["local_storage"] = {
            "status": "PASS" if media_writable else "WARNING",
            "media_root": media_path,
            "writable": media_writable
        }

        # 3. Core Engine Telemetry
        try:
            user_count = User.objects.count()
            session_count = ExamSession.objects.count()
            timetable_count = Timetable.objects.count()
            tickets_count = HallTicket.objects.count()

            diagnostics["telemetry"] = {
                "registered_users": user_count,
                "exam_sessions": session_count,
                "timetables_computed": timetable_count,
                "hall_tickets_issued": tickets_count
            }
        except Exception:
            diagnostics["telemetry"] = "Unavailable during migration"

        diagnostics["total_response_time_ms"] = round((time.time() - start_time) * 1000, 2)

        http_status = status.HTTP_200_OK if diagnostics["status"] == "HEALTHY" else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(diagnostics, status=http_status)
