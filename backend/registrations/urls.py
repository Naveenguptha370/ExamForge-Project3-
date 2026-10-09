"""ExamForge M2 — Registrations URL Configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectRegistrationViewSet,
    ExamRegistrationViewSet,
    BulkRegistrationViewSet,
    RegistrationReportViewSet,
)
app_name = 'registrations'

router = DefaultRouter()
router.register(r'subject-registrations', SubjectRegistrationViewSet, basename='subject-registration')
router.register(r'exam-registrations',    ExamRegistrationViewSet,    basename='exam-registration')
router.register(r'bulk',                  BulkRegistrationViewSet,    basename='bulk-registration')
router.register(r'reports',               RegistrationReportViewSet,  basename='registration-report')

# Extra convenience routes
from .views import SubjectRegistrationViewSet, RegistrationReportViewSet
from django.urls import path

urlpatterns = [
    path('', include(router.urls)),
    # /registrations/dashboard/
    path(
        'dashboard/',
        SubjectRegistrationViewSet.as_view({'get': 'dashboard'}),
        name='registration-dashboard',
    ),
    # /registrations/available-subjects/
    path(
        'available-subjects/',
        SubjectRegistrationViewSet.as_view({'get': 'available_subjects'}),
        name='registration-available-subjects',
    ),
    # /registrations/reports/summary/
    path(
        'reports/summary/',
        RegistrationReportViewSet.as_view({'get': 'summary'}),
        name='registration-report-summary',
    ),
    # /registrations/reports/by-department/
    path(
        'reports/by-department/',
        RegistrationReportViewSet.as_view({'get': 'by_department'}),
        name='registration-report-dept',
    ),
    # /registrations/bulk/import/
    path(
        'bulk/import/',
        BulkRegistrationViewSet.as_view({'post': 'import_csv'}),
        name='bulk-registration-import',
    ),
]
