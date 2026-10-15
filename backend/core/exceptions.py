"""
ExamForge custom exception handling and error response formatting.
Provides a unified exception handler for Django REST Framework.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from django.db import IntegrityError

logger = logging.getLogger("examforge.exceptions")


def examforge_exception_handler(exc, context):
    """
    Custom DRF exception handler that wraps all errors in the standard
    ExamForge error envelope: {"status": "error", "error": "...", "details": {...}}
    """
    # First, let DRF handle its own exceptions
    response = exception_handler(exc, context)

    if response is not None:
        error_message = _extract_drf_error(response.data)
        response.data = {
            "status": "error",
            "error": error_message,
            "http_status": response.status_code,
            "details": response.data if isinstance(response.data, dict) else None,
        }
        return response

    # Handle Django core exceptions
    if isinstance(exc, DjangoValidationError):
        return Response({
            "status": "error",
            "error": "Validation failed.",
            "details": exc.message_dict if hasattr(exc, "message_dict") else {"non_field": exc.messages},
            "http_status": 422,
        }, status=422)

    if isinstance(exc, Http404):
        return Response({
            "status": "error",
            "error": "The requested resource was not found.",
            "http_status": 404,
        }, status=404)

    if isinstance(exc, IntegrityError):
        logger.error("IntegrityError in view %s: %s", context.get("view"), exc)
        return Response({
            "status": "error",
            "error": "A database integrity constraint was violated. Please check for duplicate entries.",
            "http_status": 409,
        }, status=409)

    # Log unexpected exceptions
    logger.exception(
        "Unhandled exception in view %s (method=%s): %s",
        context.get("view"),
        context.get("request", {}).method if context.get("request") else "?",
        exc
    )
    return Response({
        "status": "error",
        "error": "An unexpected internal error occurred. Please contact support.",
        "http_status": 500,
    }, status=500)


def _extract_drf_error(data) -> str:
    if isinstance(data, str):
        return data
    if isinstance(data, list) and data:
        return str(data[0])
    if isinstance(data, dict):
        if "detail" in data:
            return str(data["detail"])
        first_key = next(iter(data), None)
        if first_key:
            val = data[first_key]
            if isinstance(val, list):
                return f"{first_key}: {val[0]}"
            return f"{first_key}: {val}"
    return "An error occurred."


class ExamForgeAPIError(Exception):
    """Base class for ExamForge application-level API errors."""
    def __init__(self, message: str, code: str = "api_error", http_status: int = 400):
        self.message = message
        self.code = code
        self.http_status = http_status
        super().__init__(message)


class ResourceConflictError(ExamForgeAPIError):
    """Raised when a resource conflict is detected (e.g., duplicate booking)."""
    def __init__(self, message: str):
        super().__init__(message, code="resource_conflict", http_status=409)


class InsufficientCapacityError(ExamForgeAPIError):
    """Raised when hall/seating capacity is insufficient."""
    def __init__(self, message: str):
        super().__init__(message, code="insufficient_capacity", http_status=422)


class RegistrationClosedError(ExamForgeAPIError):
    """Raised when a student attempts to register after the deadline."""
    def __init__(self, deadline):
        super().__init__(
            f"Registration for this session closed on {deadline}.",
            code="registration_closed",
            http_status=403
        )
