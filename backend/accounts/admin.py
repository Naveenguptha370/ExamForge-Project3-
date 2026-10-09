from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'status', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('ExamForge', {'fields': ('role', 'phone', 'status', 'last_login_ip')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('ExamForge', {'fields': ('role', 'phone', 'status', 'last_login_ip')}),
    )
