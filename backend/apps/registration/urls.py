from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentEnrollmentViewSet, SubjectRegistrationViewSet

router = DefaultRouter()
router.register(r'enrollments', StudentEnrollmentViewSet)
router.register(r'subjects', SubjectRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
