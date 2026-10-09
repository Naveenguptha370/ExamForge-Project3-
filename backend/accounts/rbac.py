"""
ExamForge - Granular Role-Based Access Control (RBAC) Architecture
Member 1: Authentication & User Management
"""
from typing import Dict, Set, List, Optional
from enum import Enum
from django.core.exceptions import PermissionDenied

class AcademicRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    EXAM_CONTROLLER = "EXAM_CONTROLLER"
    DEAN_ACADEMICS = "DEAN_ACADEMICS"
    HOD = "HOD"
    CHIEF_SUPERINTENDENT = "CHIEF_SUPERINTENDENT"
    FACULTY_INVIGILATOR = "FACULTY_INVIGILATOR"
    EXAM_STAFF = "EXAM_STAFF"
    STUDENT = "STUDENT"

class PermissionScope(str, Enum):
    GLOBAL = "GLOBAL"
    DEPARTMENT = "DEPARTMENT"
    ASSIGNED_EXAM = "ASSIGNED_EXAM"
    OWN_PROFILE = "OWN_PROFILE"

class GranularPermissions:
    # User Management
    USER_CREATE = "user:create"
    USER_VIEW = "user:view"
    USER_UPDATE = "user:update"
    USER_DEACTIVATE = "user:deactivate"
    USER_DELETE = "user:delete"
    USER_RESET_PWD = "user:reset_password"
    USER_ROLE_ASSIGN = "user:assign_role"

    # Faculty Management
    FACULTY_CREATE = "faculty:create"
    FACULTY_VIEW = "faculty:view"
    FACULTY_UPDATE = "faculty:update"
    FACULTY_ARCHIVE = "faculty:archive"
    FACULTY_AVAILABILITY_EDIT = "faculty:availability_edit"
    FACULTY_LEAVE_APPLY = "faculty:leave_apply"
    FACULTY_LEAVE_APPROVE = "faculty:leave_approve"
    FACULTY_WORKLOAD_VIEW = "faculty:workload_view"

    # Audit & System Logs
    AUDIT_VIEW = "audit:view"
    AUDIT_EXPORT = "audit:export"

class RoleCapabilityEngine:
    """Resolves whether a role or user context holds specific granular permissions."""
    
    _ROLE_HIERARCHY: Dict[str, List[str]] = {
        AcademicRole.SUPER_ADMIN: [AcademicRole.EXAM_CONTROLLER, AcademicRole.DEAN_ACADEMICS],
        AcademicRole.EXAM_CONTROLLER: [AcademicRole.CHIEF_SUPERINTENDENT, AcademicRole.EXAM_STAFF],
        AcademicRole.DEAN_ACADEMICS: [AcademicRole.HOD],
        AcademicRole.HOD: [AcademicRole.FACULTY_INVIGILATOR],
        AcademicRole.CHIEF_SUPERINTENDENT: [AcademicRole.FACULTY_INVIGILATOR, AcademicRole.EXAM_STAFF],
        AcademicRole.FACULTY_INVIGILATOR: [],
        AcademicRole.EXAM_STAFF: [],
        AcademicRole.STUDENT: []
    }

    _ROLE_PERMISSIONS: Dict[str, Set[str]] = {
        AcademicRole.SUPER_ADMIN: {
            GranularPermissions.USER_CREATE, GranularPermissions.USER_VIEW,
            GranularPermissions.USER_UPDATE, GranularPermissions.USER_DEACTIVATE,
            GranularPermissions.USER_DELETE, GranularPermissions.USER_RESET_PWD,
            GranularPermissions.USER_ROLE_ASSIGN, GranularPermissions.FACULTY_CREATE,
            GranularPermissions.FACULTY_VIEW, GranularPermissions.FACULTY_UPDATE,
            GranularPermissions.FACULTY_ARCHIVE, GranularPermissions.FACULTY_AVAILABILITY_EDIT,
            GranularPermissions.FACULTY_LEAVE_APPLY, GranularPermissions.FACULTY_LEAVE_APPROVE,
            GranularPermissions.FACULTY_WORKLOAD_VIEW, GranularPermissions.AUDIT_VIEW,
            GranularPermissions.AUDIT_EXPORT
        },
        AcademicRole.EXAM_CONTROLLER: {
            GranularPermissions.USER_VIEW, GranularPermissions.FACULTY_VIEW,
            GranularPermissions.FACULTY_AVAILABILITY_EDIT, GranularPermissions.FACULTY_LEAVE_APPROVE,
            GranularPermissions.FACULTY_WORKLOAD_VIEW, GranularPermissions.AUDIT_VIEW
        },
        AcademicRole.HOD: {
            GranularPermissions.FACULTY_VIEW, GranularPermissions.FACULTY_AVAILABILITY_EDIT,
            GranularPermissions.FACULTY_LEAVE_APPROVE, GranularPermissions.FACULTY_WORKLOAD_VIEW
        },
        AcademicRole.FACULTY_INVIGILATOR: {
            GranularPermissions.FACULTY_VIEW, GranularPermissions.FACULTY_AVAILABILITY_EDIT,
            GranularPermissions.FACULTY_LEAVE_APPLY
        },
        AcademicRole.EXAM_STAFF: {
            GranularPermissions.FACULTY_VIEW, GranularPermissions.FACULTY_WORKLOAD_VIEW
        },
        AcademicRole.STUDENT: set()
    }

    @classmethod
    def has_permission(cls, user_role: str, permission: str, department_match: bool = True) -> bool:
        perms = cls._ROLE_PERMISSIONS.get(user_role, set())
        if permission in perms:
            return department_match
        return False

    @classmethod
    def enforce(cls, user_role: str, permission: str, department_match: bool = True) -> None:
        if not cls.has_permission(user_role, permission, department_match):
            raise PermissionDenied(f"Role '{user_role}' lacks required permission: '{permission}'.")
