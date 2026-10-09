from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvigilatorDutyViewSet, DutyRequirementViewSet

router = DefaultRouter()
router.register(r'duties', InvigilatorDutyViewSet, basename='invigilator-duty')
router.register(r'requirements', DutyRequirementViewSet, basename='duty-requirement')

urlpatterns = [
    path('', include(router.urls)),
]
