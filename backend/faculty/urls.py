from django.urls import path
from .views import FacultyAvailabilityViewSet, FacultyLeaveViewSet, FacultyProfileViewSet

faculty_profiles = FacultyProfileViewSet.as_view({'get': 'list', 'post': 'create'})
faculty_profile_detail = FacultyProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'})
faculty_availability = FacultyAvailabilityViewSet.as_view({'get': 'list', 'post': 'create'})
faculty_leave = FacultyLeaveViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('dashboard/', FacultyProfileViewSet.as_view({'get': 'dashboard'}), name='faculty-dashboard'),
    path('profiles/', faculty_profiles, name='faculty-profiles'),
    path('profiles/<int:pk>/', faculty_profile_detail, name='faculty-profile-detail'),
    path('availability/', faculty_availability, name='faculty-availability'),
    path('leave/', faculty_leave, name='faculty-leave'),
]
