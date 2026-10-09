from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyProfileViewSet, FacultyAvailabilityViewSet, FacultyLeaveViewSet

router = DefaultRouter()
router.register(r'profiles', FacultyProfileViewSet)
router.register(r'availability', FacultyAvailabilityViewSet)
router.register(r'leaves', FacultyLeaveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
