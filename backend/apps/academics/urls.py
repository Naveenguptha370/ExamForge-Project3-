from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, CourseViewSet, BranchViewSet,
    SemesterViewSet, SubjectViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'subjects', SubjectViewSet, basename='subject')

urlpatterns = [
    path('', include(router.urls)),
]
