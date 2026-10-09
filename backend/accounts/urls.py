from django.urls import path
from .views import AuditLogViewSet, LoginAPIView, LogoutAPIView, UserViewSet

user_list = UserViewSet.as_view({'get': 'list', 'post': 'create'})
user_detail = UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'})

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('me/', UserViewSet.as_view({'get': 'me'}), name='current-user'),
    path('dashboard/', UserViewSet.as_view({'get': 'dashboard'}), name='user-dashboard'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users/reset-password/', UserViewSet.as_view({'post': 'reset_password'}), name='reset-password'),
    path('audit-logs/', AuditLogViewSet.as_view({'get': 'list'}), name='audit-logs'),
]
