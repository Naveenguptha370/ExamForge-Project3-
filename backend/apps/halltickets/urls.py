from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HallTicketViewSet

router = DefaultRouter()
router.register(r'tickets', HallTicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
