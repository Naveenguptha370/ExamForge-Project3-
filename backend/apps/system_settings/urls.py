from django.urls import path
from .views import SystemSettingView

urlpatterns = [
    path('config/', SystemSettingView.as_view(), name='system-setting'),
]
