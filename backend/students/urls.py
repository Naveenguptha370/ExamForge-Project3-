"""
ExamForge M2 — Student URL Configuration
==========================================
Registers all student management API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from students.views import StudentViewSet, EnrollmentRecordViewSet

app_name = 'students'

router = DefaultRouter()
router.register(r'', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentRecordViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
