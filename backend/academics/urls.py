"""
ExamForge M2 — Academic URL Configuration
==========================================
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from academics.views import (
    AcademicYearViewSet,
    DepartmentViewSet,
    CourseViewSet,
    BranchViewSet,
    SemesterViewSet,
    SubjectViewSet,
    AcademicDashboardView,
)

app_name = 'academics'

router = DefaultRouter()
router.register(r'years', AcademicYearViewSet, basename='academic-year')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'subjects', SubjectViewSet, basename='subject')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', AcademicDashboardView.as_view({'get': 'dashboard'}), name='academic-dashboard'),
    path('structure/', AcademicDashboardView.as_view({'get': 'structure'}), name='academic-structure'),
]
