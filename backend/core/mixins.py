"""
ExamForge core mixins for Django REST Framework views.
Provides standardized response formatting, pagination, error handling,
permission checks, and audit logging across all API endpoints.
"""
import logging
import time
from typing import Optional, Type
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

logger = logging.getLogger("examforge.core.mixins")


class ExamForgePagination(PageNumberPagination):
    """Standard pagination for all ExamForge API list views."""
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 200
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })


class StandardResponseMixin:
    """
    Mixin providing standardized JSON response formatting.
    All ExamForge API views inherit this to ensure consistent output structure.

    Success:  {"status": "success", "data": {...}, "message": "..."}
    Error:    {"status": "error",   "error": "...", "details": {...}}
    """

    def success_response(
        self,
        data=None,
        message: str = "OK",
        http_status: int = status.HTTP_200_OK,
        meta: Optional[dict] = None,
    ) -> Response:
        payload = {"status": "success", "message": message}
        if data is not None:
            payload["data"] = data
        if meta:
            payload["meta"] = meta
        return Response(payload, status=http_status)

    def created_response(self, data=None, message: str = "Created successfully") -> Response:
        return self.success_response(data=data, message=message, http_status=status.HTTP_201_CREATED)

    def error_response(
        self,
        error: str,
        details=None,
        http_status: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        payload = {"status": "error", "error": error}
        if details:
            payload["details"] = details
        return Response(payload, status=http_status)

    def not_found_response(self, resource: str = "Resource") -> Response:
        return self.error_response(f"{resource} not found.", http_status=status.HTTP_404_NOT_FOUND)

    def forbidden_response(self, reason: str = "Access denied.") -> Response:
        return self.error_response(reason, http_status=status.HTTP_403_FORBIDDEN)

    def validation_error_response(self, errors) -> Response:
        return self.error_response("Validation failed.", details=errors, http_status=422)


class AuditLogMixin:
    """
    Mixin that automatically logs create/update/delete operations
    to the analytics activity log.
    """

    audit_resource_type: str = ""

    def _get_analytics_service(self):
        try:
            from analytics.service import analytics_service
            return analytics_service
        except ImportError:
            return None

    def perform_create(self, serializer):
        instance = serializer.save()
        self._log_action("create", instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._log_action("update", instance)
        return instance

    def perform_destroy(self, instance):
        self._log_action("delete", instance)
        instance.delete()

    def _log_action(self, action: str, instance):
        svc = self._get_analytics_service()
        if svc and hasattr(self, "request"):
            try:
                svc.log_activity(
                    user=self.request.user,
                    action=action,
                    resource_type=self.audit_resource_type or instance.__class__.__name__,
                    resource_id=getattr(instance, "pk", ""),
                    request=self.request,
                )
            except Exception as exc:
                logger.warning("AuditLogMixin._log_action failed: %s", exc)


class SearchFilterMixin:
    """
    Mixin for flexible search and ordering in list views.
    Subclasses define `search_fields` and `ordering_fields`.
    """
    search_fields: list[str] = []
    ordering_fields: list[str] = []
    default_ordering: str = "-created_at"

    def apply_search(self, queryset: QuerySet, search_term: str) -> QuerySet:
        if not search_term or not self.search_fields:
            return queryset
        from django.db.models import Q
        q = Q()
        for field in self.search_fields:
            q |= Q(**{f"{field}__icontains": search_term})
        return queryset.filter(q)

    def apply_ordering(self, queryset: QuerySet, order_param: str) -> QuerySet:
        if not order_param:
            return queryset.order_by(self.default_ordering)
        direction = ""
        field = order_param
        if order_param.startswith("-"):
            direction = "-"
            field = order_param[1:]
        if field in self.ordering_fields:
            return queryset.order_by(f"{direction}{field}")
        return queryset.order_by(self.default_ordering)

    def get_filtered_queryset(self, queryset: QuerySet, request) -> QuerySet:
        search = request.query_params.get("q", "").strip()
        order = request.query_params.get("order_by", "")
        qs = self.apply_search(queryset, search)
        qs = self.apply_ordering(qs, order)
        return qs


class PerformanceTimingMixin:
    """
    Mixin that adds X-ExamForge-Duration header to all responses
    for API performance monitoring.
    """

    def dispatch(self, request, *args, **kwargs):
        start = time.time()
        response = super().dispatch(request, *args, **kwargs)
        duration_ms = int((time.time() - start) * 1000)
        response["X-ExamForge-Duration"] = f"{duration_ms}ms"
        if duration_ms > 2000:
            logger.warning(
                "SLOW API: %s %s took %dms (user=%s)",
                request.method, request.path, duration_ms,
                getattr(request.user, "email", "anonymous")
            )
        return response


class RequireRoleMixin:
    """
    Mixin that enforces role-based access at the view level.
    Subclasses set `required_roles = ["Admin", "ExamCoordinator"]`.
    """
    required_roles: list[str] = []

    def check_role_permission(self, request: Request) -> bool:
        if not self.required_roles:
            return True
        if request.user.is_superuser:
            return True
        user_groups = set(request.user.groups.values_list("name", flat=True))
        return bool(user_groups.intersection(set(self.required_roles)))

    def dispatch(self, request, *args, **kwargs):
        if not self.check_role_permission(request):
            return Response(
                {"status": "error", "error": "Insufficient role permissions."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().dispatch(request, *args, **kwargs)


class BulkOperationMixin(StandardResponseMixin):
    """
    Mixin for bulk create/update/delete operations.
    Handles partial failures gracefully and returns per-item results.
    """

    def bulk_create(self, serializer_class, data_list: list, **save_kwargs) -> dict:
        created, errors = [], []
        for i, item_data in enumerate(data_list):
            ser = serializer_class(data=item_data)
            if ser.is_valid():
                try:
                    obj = ser.save(**save_kwargs)
                    created.append({"index": i, "id": str(getattr(obj, "pk", "")), "status": "created"})
                except Exception as exc:
                    errors.append({"index": i, "error": str(exc)})
            else:
                errors.append({"index": i, "errors": ser.errors})

        return {
            "total": len(data_list),
            "created": len(created),
            "failed": len(errors),
            "results": created,
            "errors": errors,
        }

    def bulk_delete(self, queryset: QuerySet, id_list: list) -> dict:
        to_delete = queryset.filter(pk__in=id_list)
        found_ids = set(str(pk) for pk in to_delete.values_list("pk", flat=True))
        missing = [str(i) for i in id_list if str(i) not in found_ids]
        count, _ = to_delete.delete()
        return {
            "requested": len(id_list),
            "deleted": count,
            "not_found": missing,
        }
