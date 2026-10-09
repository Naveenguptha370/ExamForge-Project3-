from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, LogoutView, CurrentUserProfileView,
    PasswordChangeView, UserManagementViewSet, UserActivityListView
)

router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('me/', CurrentUserProfileView.as_view(), name='auth-me'),
    path('change-password/', PasswordChangeView.as_view(), name='auth-change-password'),
    path('activities/', UserActivityListView.as_view(), name='auth-activities'),
    path('', include(router.urls)),
]
