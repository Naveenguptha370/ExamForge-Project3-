from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlockViewSet, RoomViewSet, RoomAvailabilityViewSet

router = DefaultRouter()
router.register(r'blocks', BlockViewSet, basename='block')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'availabilities', RoomAvailabilityViewSet, basename='room-availability')

urlpatterns = [
    path('', include(router.urls)),
]
