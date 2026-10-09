from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamAttendanceSheetViewSet, AttendanceRecordViewSet

router = DefaultRouter()
router.register(r'sheets', ExamAttendanceSheetViewSet)
router.register(r'records', AttendanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
