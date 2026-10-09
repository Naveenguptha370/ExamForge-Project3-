"""
ExamForge URL Configuration
Integrated Five-Member Architecture
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Member 1: Auth & Faculty
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/faculty/', include('apps.faculty.urls')),

    # Member 2: Academics, Students & Registration
    path('api/academics/', include('apps.academics.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/registration/', include('apps.registration.urls')),

    # Member 3: Examinations & Scheduling
    path('api/examinations/', include('apps.examinations.urls')),
    path('api/scheduling/', include('apps.scheduling.urls')),

    # Member 4: Infrastructure, Seating & Invigilation
    path('api/infrastructure/', include('apps.infrastructure.urls')),
    path('api/seating/', include('apps.seating.urls')),
    path('api/invigilation/', include('apps.invigilation.urls')),

    # Member 5: Hall Tickets, Attendance, Notifications, Analytics, Audit & Settings
    path('api/halltickets/', include('apps.halltickets.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/audit/', include('apps.audit.urls')),
    path('api/settings/', include('apps.system_settings.urls')),
    path('api/health/', include('apps.system_settings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
