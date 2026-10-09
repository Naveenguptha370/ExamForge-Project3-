from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, CurrentUserView, ChangePasswordView, UserViewSet, UserActivityLogViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'activity', UserActivityLogViewSet, basename='user-activity')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('', include(router.urls)),
]
