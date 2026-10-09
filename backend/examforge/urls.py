"""
ExamForge URL Configuration.
Exposes internal REST endpoints for all 5 integrated modules.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root_view(request):
    return JsonResponse({
        'system': 'ExamForge — Examination Operations System',
        'version': '1.0.0',
        'status': 'Operational',
        'modules': {
            'member_1_auth_faculty': '/api/auth/, /api/faculty/',
            'member_2_students_academics': '/api/academics/, /api/students/',
            'member_3_examinations_scheduling': '/api/examinations/, /api/scheduling/',
            'member_4_infrastructure_seating_invigilation': '/api/infrastructure/, /api/seating/, /api/invigilation/',
            'member_5_halltickets_attendance_audit_reports': '/api/halltickets/, /api/attendance/, /api/notifications/, /api/analytics/, /api/audit/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root_view, name='api-root'),
    
    # Member 1 endpoints
    path('api/auth/', include('apps.accounts.urls')),
    path('api/faculty/', include('apps.faculty.urls')),
    
    # Member 2 endpoints
    path('api/academics/', include('apps.academics.urls')),
    path('api/students/', include('apps.students.urls')),
    
    # Member 3 endpoints (Primary Focus)
    path('api/examinations/', include('apps.examinations.urls')),
    path('api/scheduling/', include('apps.scheduling.urls')),
    
    # Member 4 endpoints
    path('api/infrastructure/', include('apps.infrastructure.urls')),
    path('api/seating/', include('apps.seating.urls')),
    path('api/invigilation/', include('apps.invigilation.urls')),
    
    # Member 5 endpoints
    path('api/halltickets/', include('apps.halltickets.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/audit/', include('apps.audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
