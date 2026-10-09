from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeatingPlanViewSet, RoomAllocationViewSet, SeatAssignmentViewSet

router = DefaultRouter()
router.register(r'plans', SeatingPlanViewSet, basename='seating-plan')
router.register(r'room-allocations', RoomAllocationViewSet, basename='room-allocation')
router.register(r'assignments', SeatAssignmentViewSet, basename='seat-assignment')

urlpatterns = [
    path('', include(router.urls)),
]
