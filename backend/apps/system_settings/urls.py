from django.urls import path
from .views import SystemSettingView
from .health import SystemHealthView

urlpatterns = [
    path('config/', SystemSettingView.as_view(), name='system-setting'),
    path('health/', SystemHealthView.as_view(), name='system-health'),
]
