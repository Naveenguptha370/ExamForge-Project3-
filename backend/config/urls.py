"""
ExamForge M2 — Root URL Configuration
========================================
Registers all M2 application routes under /api/v1/ prefix.
Integrates with M1's auth routes without duplicating them.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# ─── API v1 URL Patterns ─────────────────────────────────────────────────────────
api_v1_patterns = [
    # ── M1 Authentication (reuse — do not duplicate) ──────────────────────────
    # path('auth/', include('accounts.urls')),   # Activated when M1 is integrated
    # path('faculty/', include('faculty.urls')),  # Activated when M1 is integrated

    # ── M2: Student Management ────────────────────────────────────────────────
    path('students/', include('students.urls', namespace='students')),

    # ── M2: Academic Management ───────────────────────────────────────────────
    path('academics/', include('academics.urls', namespace='academics')),

    # ── M2: Subject & Exam Registration ──────────────────────────────────────
    path('registrations/', include('registrations.urls', namespace='registrations')),

    # ── M3: Examination (Integration stubs — activate when M3 is ready) ──────
    # path('examinations/', include('examinations.urls')),

    # ── API Schema & Documentation ────────────────────────────────────────────
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='redoc'),
]

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API Version 1
    path('api/v1/', include(api_v1_patterns)),

    # Health Check
    path('api/v1/health/', include('config.health_urls')),
]

# ─── Debug Toolbar ───────────────────────────────────────────────────────────────
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
