from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExamSessionViewSet, TimeSlotViewSet,
    ExamSubjectConfigViewSet, SchedulingConstraintConfigViewSet
)

router = DefaultRouter()
router.register(r'sessions', ExamSessionViewSet, basename='exam-session')
router.register(r'timeslots', TimeSlotViewSet, basename='time-slot')
router.register(r'subject-configs', ExamSubjectConfigViewSet, basename='subject-config')
router.register(r'constraints', SchedulingConstraintConfigViewSet, basename='constraint-config')

urlpatterns = [
    path('', include(router.urls)),
]
