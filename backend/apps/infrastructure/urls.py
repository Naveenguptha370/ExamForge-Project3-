from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet, ExaminationRoomViewSet, RoomAvailabilityViewSet

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet)
router.register(r'rooms', ExaminationRoomViewSet)
router.register(r'availability', RoomAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
