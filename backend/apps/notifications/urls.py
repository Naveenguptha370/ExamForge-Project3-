from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, SystemNotificationViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'alerts', SystemNotificationViewSet, basename='system-notification')

urlpatterns = [
    path('', include(router.urls)),
]
