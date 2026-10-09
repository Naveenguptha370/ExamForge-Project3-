from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, SubjectRegistrationViewSet

router = DefaultRouter()
router.register(r'records', StudentViewSet, basename='student-record')
router.register(r'registrations', SubjectRegistrationViewSet, basename='subject-registration')

urlpatterns = [
    path('', include(router.urls)),
]
