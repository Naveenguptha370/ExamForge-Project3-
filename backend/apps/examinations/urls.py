from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamSessionViewSet, TimeSlotViewSet, ExamSubjectViewSet

router = DefaultRouter()
router.register(r'sessions', ExamSessionViewSet)
router.register(r'timeslots', TimeSlotViewSet)
router.register(r'subjects', ExamSubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
