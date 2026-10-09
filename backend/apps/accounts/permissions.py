from rest_framework import permissions
from .models import UserRole

class IsAdminUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == UserRole.ADMIN or request.user.is_superuser))

class IsFacultyRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == UserRole.FACULTY or request.user.role == UserRole.ADMIN or request.user.is_superuser))

class IsExamStaffRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role in [UserRole.ADMIN, UserRole.EXAM_STAFF] or request.user.is_superuser))

class IsStudentRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.STUDENT)

class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role in [UserRole.ADMIN, UserRole.EXAM_STAFF, UserRole.FACULTY] or request.user.is_superuser))
