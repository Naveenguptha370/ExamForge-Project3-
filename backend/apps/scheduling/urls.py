from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TimetableViewSet, TimetableEntryViewSet,
    SchedulingClashViewSet, TimetableRevisionViewSet
)

router = DefaultRouter()
router.register(r'timetables', TimetableViewSet, basename='timetable')
router.register(r'entries', TimetableEntryViewSet, basename='timetable-entry')
router.register(r'clashes', SchedulingClashViewSet, basename='scheduling-clash')
router.register(r'revisions', TimetableRevisionViewSet, basename='timetable-revision')

urlpatterns = [
    path('', include(router.urls)),
]
