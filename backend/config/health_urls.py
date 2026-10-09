"""ExamForge M2 — Health Check URLs and Views"""
from django.urls import path
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    db_ok = True
    try:
        connection.ensure_connection()
    except Exception:
        db_ok = False

    return JsonResponse({
        "status": "ok" if db_ok else "degraded",
        "service": "examforge-m2",
        "database": "connected" if db_ok else "unreachable",
        "module": "M2 (Academics, Students, Registrations)"
    }, status=200 if db_ok else 503)

urlpatterns = [
    path('', health_check, name='health-check'),
]
