"""
ExamForge M2 — Student Management Permissions
===============================================
Custom DRF permission classes for the students module.
All permissions integrate with M1's role-based user model.

M1 integration assumption:
- User model has a 'role' field with values:
    'admin', 'exam_staff', 'faculty', 'student'
- This aligns with M1's role definitions.
- If M1 uses a different role field name, update ROLE_FIELD below.

If M1's role system is not yet deployed, the permissions below
gracefully fall back to checking Django's is_staff and is_superuser.
"""

import logging
from rest_framework.permissions import BasePermission, IsAuthenticated

logger = logging.getLogger(__name__)

# ─── M1 Role Integration ──────────────────────────────────────────────────────────
# Update this if M1 uses a different attribute name for roles.
ROLE_FIELD = 'role'

ADMIN_ROLES = {'admin', 'superadmin'}
EXAM_STAFF_ROLES = {'exam_staff', 'examination_staff'}
FACULTY_ROLES = {'faculty', 'invigilator'}
STUDENT_ROLES = {'student'}
ALL_STAFF_ROLES = ADMIN_ROLES | EXAM_STAFF_ROLES | FACULTY_ROLES


def get_user_role(user):
    """Safely extract the user role, falling back to Django permissions."""
    if not user or not user.is_authenticated:
        return None
    role = getattr(user, ROLE_FIELD, None)
    if role:
        return role.lower()
    # Fallback: use Django's built-in flags
    if user.is_superuser:
        return 'admin'
    if user.is_staff:
        return 'exam_staff'
    return 'student'


def is_admin(user):
    return get_user_role(user) in ADMIN_ROLES


def is_exam_staff(user):
    return get_user_role(user) in EXAM_STAFF_ROLES


def is_faculty(user):
    return get_user_role(user) in FACULTY_ROLES


def is_student(user):
    return get_user_role(user) in STUDENT_ROLES


def is_admin_or_exam_staff(user):
    return get_user_role(user) in (ADMIN_ROLES | EXAM_STAFF_ROLES)


# ─── Permission Classes ───────────────────────────────────────────────────────────

class IsAdminOrExamStaff(BasePermission):
    """
    Allows access only to administrators and examination staff.
    Blocks faculty and student roles.
    """
    message = 'Only administrators and examination staff can perform this action.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return is_admin_or_exam_staff(request.user)


class IsAdminOrExamStaffOrReadOnly(BasePermission):
    """
    Allows read access to all authenticated users.
    Write access is restricted to admins and exam staff.
    """
    message = 'Only administrators and examination staff can modify this resource.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return is_admin_or_exam_staff(request.user)


class CanImportStudents(BasePermission):
    """Specific permission for the CSV bulk import action."""
    message = 'Only administrators can import student records in bulk.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return is_admin(request.user)


class CanViewStudent(BasePermission):
    """
    Controls who can view student records.
    - Admins and exam staff: can view all.
    - Faculty: can view students in their department.
    - Students: can view only their own profile.
    """
    message = 'You do not have permission to view this student record.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = get_user_role(user)

        if role in ADMIN_ROLES | EXAM_STAFF_ROLES:
            return True

        if role in FACULTY_ROLES:
            faculty_dept = getattr(user, 'department_id', None)
            if faculty_dept:
                return obj.department_id == faculty_dept
            return False

        if role in STUDENT_ROLES:
            # Students can only see their own profile
            own_profile = getattr(user, 'student_profile', None)
            if own_profile:
                return own_profile.pk == obj.pk
            return False

        return False


class CanManageStudentStatus(BasePermission):
    """Controls who can activate/deactivate students."""
    message = 'Only administrators can change student status.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return is_admin(request.user)


class IsOwnerOrAdminOrExamStaff(BasePermission):
    """
    Object-level permission.
    Allows access to the student themselves, admins, and exam staff.
    """
    message = 'Access denied.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = get_user_role(user)

        if role in ADMIN_ROLES | EXAM_STAFF_ROLES:
            return True

        own_profile = getattr(user, 'student_profile', None)
        if own_profile and own_profile.pk == obj.pk:
            return True

        return False
