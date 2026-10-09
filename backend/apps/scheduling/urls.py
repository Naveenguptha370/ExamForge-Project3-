from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimetableViewSet, TimetableEntryViewSet

router = DefaultRouter()
router.register(r'timetables', TimetableViewSet)
router.register(r'entries', TimetableEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
