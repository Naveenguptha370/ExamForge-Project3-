"""
ExamForge custom DRF permissions.
Role-based and object-level permission classes used across all API views.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsExamCoordinator(BasePermission):
    """Allow access only to users with the ExamCoordinator role."""
    message = "Only ExamCoordinators may perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="ExamCoordinator").exists()
        )


class IsFacultyOrAbove(BasePermission):
    """Allow Faculty, ExamCoordinator, and Admin."""
    message = "Faculty or higher role required."
    ALLOWED_ROLES = {"Faculty", "ExamCoordinator", "Admin"}

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return bool(
            request.user.groups.filter(name__in=self.ALLOWED_ROLES).exists()
        )


class IsOwnerOrAdmin(BasePermission):
    """Allow access only to the owner of an object or admin users."""
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        owner_field = getattr(view, "owner_field", "user")
        owner = getattr(obj, owner_field, None)
        if owner is None:
            return False
        return owner == request.user


class ReadOnly(BasePermission):
    """Allow GET, HEAD, OPTIONS to any authenticated user."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Allow read for authenticated users, write for admins only."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser


class DenyAll(BasePermission):
    """Deny all access — useful for temporarily locking an endpoint."""
    message = "This endpoint is currently disabled."
    def has_permission(self, request, view):
        return False
