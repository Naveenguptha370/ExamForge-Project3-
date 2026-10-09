"""
ExamForge - Granular Role-Based Access Control (RBAC) Architecture
Member 1: Authentication & User Management
"""
from typing import Dict, Set, List
from enum import Enum
from django.core.exceptions import PermissionDenied

class AcademicRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    EXAM_CONTROLLER = "EXAM_CONTROLLER"
    DEAN_ACADEMICS = "DEAN_ACADEMICS"
    HOD = "HOD"
    FACULTY_INVIGILATOR = "FACULTY_INVIGILATOR"
    EXAM_STAFF = "EXAM_STAFF"
    STUDENT = "STUDENT"

class GranularPermissions:
    USER_CREATE = "user:create"
    USER_VIEW = "user:view"
    USER_UPDATE = "user:update"
    USER_DEACTIVATE = "user:deactivate"
    USER_DELETE = "user:delete"
    USER_RESET_PWD = "user:reset_password"
    FACULTY_CREATE = "faculty:create"
    FACULTY_VIEW = "faculty:view"
    FACULTY_UPDATE = "faculty:update"
    FACULTY_AVAILABILITY_EDIT = "faculty:availability_edit"
    FACULTY_LEAVE_APPLY = "faculty:leave_apply"
    FACULTY_LEAVE_APPROVE = "faculty:leave_approve"
    AUDIT_VIEW = "audit:view"

class RoleCapabilityEngine:
    _ROLE_PERMISSIONS: Dict[str, Set[str]] = {
        AcademicRole.SUPER_ADMIN: {
            GranularPermissions.USER_CREATE, GranularPermissions.USER_VIEW,
            GranularPermissions.USER_UPDATE, GranularPermissions.USER_DEACTIVATE,
            GranularPermissions.USER_DELETE, GranularPermissions.USER_RESET_PWD,
            GranularPermissions.FACULTY_CREATE, GranularPermissions.FACULTY_VIEW,
            GranularPermissions.FACULTY_UPDATE, GranularPermissions.FACULTY_AVAILABILITY_EDIT,
            GranularPermissions.FACULTY_LEAVE_APPLY, GranularPermissions.FACULTY_LEAVE_APPROVE,
            GranularPermissions.AUDIT_VIEW
        },
        AcademicRole.EXAM_CONTROLLER: {
            GranularPermissions.USER_VIEW, GranularPermissions.FACULTY_VIEW,
            GranularPermissions.FACULTY_AVAILABILITY_EDIT, GranularPermissions.FACULTY_LEAVE_APPROVE,
            GranularPermissions.AUDIT_VIEW
        },
        AcademicRole.HOD: {
            GranularPermissions.FACULTY_VIEW, GranularPermissions.FACULTY_AVAILABILITY_EDIT,
            GranularPermissions.FACULTY_LEAVE_APPROVE
        },
        AcademicRole.FACULTY_INVIGILATOR: {
            GranularPermissions.FACULTY_VIEW, GranularPermissions.FACULTY_AVAILABILITY_EDIT,
            GranularPermissions.FACULTY_LEAVE_APPLY
        },
        AcademicRole.EXAM_STAFF: { GranularPermissions.FACULTY_VIEW },
        AcademicRole.STUDENT: set()
    }

    @classmethod
    def has_permission(cls, user_role: str, permission: str) -> bool:
        perms = cls._ROLE_PERMISSIONS.get(user_role, set())
        return permission in perms

    @classmethod
    def enforce(cls, user_role: str, permission: str) -> None:
        if not cls.has_permission(user_role, permission):
            raise PermissionDenied(f"Role '{user_role}' lacks required permission: '{permission}'.")
