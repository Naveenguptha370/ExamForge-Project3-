from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyProfileViewSet, FacultyAvailabilityViewSet, FacultyLeaveViewSet

router = DefaultRouter()
router.register(r'profiles', FacultyProfileViewSet, basename='faculty-profile')
router.register(r'availabilities', FacultyAvailabilityViewSet, basename='faculty-availability')
router.register(r'leaves', FacultyLeaveViewSet, basename='faculty-leave')

urlpatterns = [
    path('', include(router.urls)),
]
