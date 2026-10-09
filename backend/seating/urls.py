from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeatingPlanViewSet, SeatAllocationViewSet

router = DefaultRouter()
router.register(r'plans', SeatingPlanViewSet, basename='seating-plan')
router.register(r'allocations', SeatAllocationViewSet, basename='seat-allocation')

urlpatterns = [
    path('', include(router.urls)),
]
