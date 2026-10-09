from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, RoomViewSet, RoomMaintenanceViewSet, RoomAssignmentViewSet, RoomUtilizationView

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'maintenance', RoomMaintenanceViewSet, basename='maintenance')
router.register(r'assignments', RoomAssignmentViewSet, basename='assignment')

urlpatterns = [
    path('utilization/', RoomUtilizationView.as_view(), name='room-utilization'),
    path('', include(router.urls)),
]
