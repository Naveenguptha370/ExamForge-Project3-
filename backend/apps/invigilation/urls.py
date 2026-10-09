from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvigilatorDutyViewSet

router = DefaultRouter()
router.register(r'duties', InvigilatorDutyViewSet, basename='invigilator-duty')

urlpatterns = [
    path('', include(router.urls)),
]
