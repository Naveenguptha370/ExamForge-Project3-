"""
ExamForge M2 — Custom Exception Handler
==========================================
Provides consistent, descriptive error responses across all M2 API endpoints.
All errors follow the same JSON shape so the React frontend can handle them uniformly.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, DatabaseError
from django.http import Http404
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    ValidationError,
    Throttled,
    MethodNotAllowed,
    ParseError,
    UnsupportedMediaType,
)

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats all errors into a consistent response shape:

    {
        "status": "error",
        "code": <http_status_code>,
        "error_type": <error_class_name>,
        "message": <human-readable summary>,
        "details": <field-level errors or additional info>,
        "request_id": <optional>
    }
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    request = context.get('request')
    view = context.get('view')

    # Get request ID if available
    request_id = getattr(request, 'id', None) if request else None

    # ── Handle DRF exceptions ──────────────────────────────────────────────────
    if response is not None:
        error_type = exc.__class__.__name__
        message = _extract_message(exc)
        details = _extract_details(exc, response)

        logger.warning(
            'API Exception',
            extra={
                'error_type': error_type,
                'status_code': response.status_code,
                'path': request.path if request else None,
                'method': request.method if request else None,
                'user': str(request.user) if request else None,
            }
        )

        response.data = {
            'status': 'error',
            'code': response.status_code,
            'error_type': error_type,
            'message': message,
            'details': details,
            'request_id': request_id,
        }
        return response

    # ── Handle Django ValidationError ─────────────────────────────────────────
    if isinstance(exc, DjangoValidationError):
        logger.warning('Django ValidationError: %s', str(exc))
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'error_type': 'ValidationError',
                'message': 'Validation failed.',
                'details': exc.message_dict if hasattr(exc, 'message_dict') else {'error': exc.messages},
                'request_id': request_id,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ── Handle IntegrityError ──────────────────────────────────────────────────
    if isinstance(exc, IntegrityError):
        logger.error('Database IntegrityError: %s', str(exc))
        detail = _parse_integrity_error(exc)
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_409_CONFLICT,
                'error_type': 'IntegrityError',
                'message': detail,
                'details': {},
                'request_id': request_id,
            },
            status=status.HTTP_409_CONFLICT
        )

    # ── Handle Http404 ─────────────────────────────────────────────────────────
    if isinstance(exc, Http404):
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'error_type': 'NotFound',
                'message': 'The requested resource was not found.',
                'details': {},
                'request_id': request_id,
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ── Handle DatabaseError ───────────────────────────────────────────────────
    if isinstance(exc, DatabaseError):
        logger.critical('Unexpected DatabaseError: %s', str(exc), exc_info=True)
        return Response(
            {
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error_type': 'DatabaseError',
                'message': 'A database error occurred. Please try again later.',
                'details': {},
                'request_id': request_id,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # ── Log unexpected exceptions ──────────────────────────────────────────────
    logger.exception('Unhandled exception in view: %s', exc)
    return None


def _extract_message(exc):
    """Extract a human-readable message from the exception."""
    if isinstance(exc, AuthenticationFailed):
        return 'Authentication failed. Please check your credentials.'
    if isinstance(exc, NotAuthenticated):
        return 'Authentication is required to access this resource.'
    if isinstance(exc, PermissionDenied):
        return 'You do not have permission to perform this action.'
    if isinstance(exc, NotFound):
        return 'The requested resource was not found.'
    if isinstance(exc, ValidationError):
        return 'The submitted data contains one or more validation errors.'
    if isinstance(exc, Throttled):
        wait = getattr(exc, 'wait', None)
        if wait:
            return f'Request limit exceeded. Please wait {int(wait)} seconds before retrying.'
        return 'Request limit exceeded. Please slow down.'
    if isinstance(exc, MethodNotAllowed):
        return f'HTTP method not allowed for this endpoint.'
    if isinstance(exc, ParseError):
        return 'Malformed request data. Could not parse the request body.'
    if isinstance(exc, UnsupportedMediaType):
        return 'Unsupported media type. Please use application/json.'

    detail = getattr(exc, 'detail', None)
    if detail:
        if isinstance(detail, str):
            return detail
        if isinstance(detail, list) and detail:
            first = detail[0]
            return str(first) if not hasattr(first, 'string') else first.string
    return 'An unexpected error occurred.'


def _extract_details(exc, response):
    """Extract field-level error details for validation errors."""
    if isinstance(exc, ValidationError):
        detail = exc.detail
        if isinstance(detail, dict):
            return {
                field: [str(e) for e in errors] if isinstance(errors, list) else [str(errors)]
                for field, errors in detail.items()
            }
        if isinstance(detail, list):
            return {'non_field_errors': [str(e) for e in detail]}
    return {}


def _parse_integrity_error(exc):
    """Parse PostgreSQL integrity error messages into human-readable text."""
    error_str = str(exc).lower()
    if 'unique' in error_str:
        if 'roll_number' in error_str:
            return 'A student with this roll number already exists.'
        if 'email' in error_str:
            return 'This email address is already in use.'
        if 'student_id' in error_str:
            return 'A student with this student ID already exists.'
        if 'code' in error_str:
            return 'A record with this code already exists.'
        return 'A record with these details already exists.'
    if 'foreign key' in error_str:
        return 'This operation cannot be completed because related records depend on this entry.'
    if 'not null' in error_str:
        return 'A required field is missing.'
    return 'A database constraint violation occurred.'
