from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvigilatorDutyViewSet

router = DefaultRouter()
router.register(r'duties', InvigilatorDutyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
