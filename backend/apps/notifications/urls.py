from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, InAppNotificationViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)
router.register(r'messages', InAppNotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
