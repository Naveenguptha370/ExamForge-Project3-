"""
NotificationService — core dispatch layer for ExamForge notifications.
Supports in-app delivery, email queuing, preference filtering, and batch dispatch.
"""
import logging
from datetime import timedelta
from typing import Optional, Union
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import (
    Notification, NotificationQueue, NotificationCategory,
    NotificationTemplate, NotificationPreference, NotificationBatch,
)

logger = logging.getLogger("examforge.notifications")
User = get_user_model()


class NotificationService:
    """
    Central service for dispatching ExamForge notifications.

    Usage:
        svc = NotificationService()
        svc.notify_user(user_id=42, template_code="exam.timetable.published",
                        context={"exam_name": "Mid-Semester 2026", "date": "2026-10-20"})
    """

    def __init__(self):
        self._template_cache: dict = {}

    # ── Public dispatch API ──────────────────────────────────────

    @transaction.atomic
    def notify_user(
        self,
        user_id: int,
        template_code: str,
        context: dict,
        action_url: str = "",
        action_label: str = "",
        expires_hours: Optional[int] = None,
        priority: int = 3,
    ) -> Optional[Notification]:
        """
        Deliver a notification to a single user.

        Args:
            user_id: Target user's primary key.
            template_code: NotificationTemplate.code identifier.
            context: Dict of variable substitutions for the template.
            action_url: Optional deep-link URL shown on the notification.
            action_label: CTA button label.
            expires_hours: Hours until notification auto-expires (None = never).
            priority: 1=Critical, 2=High, 3=Normal, 4=Low

        Returns:
            Created Notification instance, or None if preference-blocked.
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.warning("notify_user: user %s not found", user_id)
            return None

        template = self._get_template(template_code)
        if template is None:
            logger.error("notify_user: template '%s' not found", template_code)
            return None

        if not self._user_allows_channel(user, template.category, "in_app"):
            logger.debug("notify_user: user %s blocked in-app for category %s", user_id, template.category)
            return None

        subject, body = template.render(context)
        expires_at = None
        if expires_hours:
            expires_at = timezone.now() + timedelta(hours=expires_hours)

        notification = Notification.objects.create(
            recipient=user,
            category=template.category,
            subject=subject,
            body=body,
            action_url=action_url,
            action_label=action_label,
            expires_at=expires_at,
            metadata={"template_code": template_code, "context": context},
        )
        logger.info("Notification %s dispatched to user %s", notification.id, user_id)
        return notification

    @transaction.atomic
    def notify_users(
        self,
        user_ids: list[int],
        template_code: str,
        context: dict,
        **kwargs,
    ) -> list[Notification]:
        """Dispatch the same notification to multiple users."""
        created = []
        for uid in user_ids:
            n = self.notify_user(uid, template_code, context, **kwargs)
            if n:
                created.append(n)
        logger.info("Bulk notify: %d notifications dispatched (of %d targets)", len(created), len(user_ids))
        return created

    @transaction.atomic
    def notify_by_role(
        self,
        role: str,
        template_code: str,
        context: dict,
        **kwargs,
    ) -> list[Notification]:
        """Notify all active users that have a specific role."""
        user_ids = list(User.objects.filter(
            groups__name=role, is_active=True
        ).values_list("id", flat=True))
        return self.notify_users(user_ids, template_code, context, **kwargs)

    def queue_email(
        self,
        user: User,
        template: NotificationTemplate,
        context: dict,
        priority: int = 3,
        scheduled_at=None,
    ) -> NotificationQueue:
        """Queue an email notification for async delivery."""
        subject, body = template.render(context)
        return NotificationQueue.objects.create(
            recipient=user,
            template=template,
            category=template.category,
            channel="email",
            priority=priority,
            subject=subject,
            body=body,
            context_data=context,
            scheduled_at=scheduled_at or timezone.now(),
        )

    # ── Batch dispatch ──────────────────────────────────────

    @transaction.atomic
    def dispatch_batch(self, batch: NotificationBatch) -> dict:
        """
        Process a NotificationBatch and deliver to all targeted recipients.

        Returns:
            Summary dict with sent, failed, skipped counts.
        """
        batch.status = "running"
        batch.started_at = timezone.now()
        batch.save(update_fields=["status", "started_at"])

        sent, failed, skipped = 0, 0, 0
        target_ids = self._resolve_batch_targets(batch)
        batch.total_recipients = len(target_ids)
        batch.save(update_fields=["total_recipients"])

        for uid in target_ids:
            try:
                n = self.notify_user(uid, batch.template.code, batch.context_data)
                if n:
                    sent += 1
                else:
                    skipped += 1
            except Exception as exc:
                logger.exception("Batch %s: failed for user %s: %s", batch.id, uid, exc)
                failed += 1

        batch.sent_count = sent
        batch.failed_count = failed
        batch.status = "completed" if failed == 0 else "failed"
        batch.completed_at = timezone.now()
        batch.save(update_fields=["sent_count", "failed_count", "status", "completed_at"])

        return {"sent": sent, "failed": failed, "skipped": skipped}

    # ── Read / management ──────────────────────────────────────

    def get_unread_count(self, user: User) -> int:
        """Return unread notification count for a user."""
        return Notification.objects.filter(
            recipient=user, is_read=False, is_archived=False
        ).exclude(
            expires_at__lt=timezone.now()
        ).count()

    def mark_all_read(self, user: User) -> int:
        """Mark all unread notifications as read. Returns count updated."""
        updated = Notification.objects.filter(
            recipient=user, is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return updated

    def archive_old(self, user: User, days: int = 30) -> int:
        """Archive notifications older than `days` days."""
        cutoff = timezone.now() - timedelta(days=days)
        return Notification.objects.filter(
            recipient=user, created_at__lt=cutoff, is_archived=False
        ).update(is_archived=True)

    def get_user_notifications(
        self,
        user: User,
        category_code: Optional[str] = None,
        unread_only: bool = False,
        limit: int = 50,
    ) -> QuerySet:
        qs = Notification.objects.filter(recipient=user, is_archived=False)
        if category_code:
            qs = qs.filter(category__code=category_code)
        if unread_only:
            qs = qs.filter(is_read=False)
        return qs.select_related("category").order_by("-created_at")[:limit]

    # ── Preferences ──────────────────────────────────────

    def update_preferences(self, user: User, preferences: dict) -> list[NotificationPreference]:
        """
        Update user notification preferences.

        preferences format:
            {
                "exam": {"in_app": true, "email": true, "sms": false},
                "seating": {"in_app": true, "email": false},
            }
        """
        updated = []
        for cat_code, prefs in preferences.items():
            try:
                category = NotificationCategory.objects.get(code=cat_code)
            except NotificationCategory.DoesNotExist:
                logger.warning("update_preferences: unknown category '%s'", cat_code)
                continue
            pref, _ = NotificationPreference.objects.get_or_create(
                user=user, category=category
            )
            if "in_app" in prefs:
                pref.in_app_enabled = prefs["in_app"]
            if "email" in prefs:
                pref.email_enabled = prefs["email"]
            if "sms" in prefs:
                pref.sms_enabled = prefs["sms"]
            if "push" in prefs:
                pref.push_enabled = prefs["push"]
            pref.save()
            updated.append(pref)
        return updated

    # ── Internal helpers ──────────────────────────────────────

    def _get_template(self, code: str) -> Optional[NotificationTemplate]:
        if code not in self._template_cache:
            try:
                self._template_cache[code] = NotificationTemplate.objects.select_related("category").get(
                    code=code, is_active=True
                )
            except NotificationTemplate.DoesNotExist:
                return None
        return self._template_cache[code]

    def _user_allows_channel(self, user: User, category: NotificationCategory, channel: str) -> bool:
        try:
            pref = NotificationPreference.objects.get(user=user, category=category)
            channel_map = {
                "in_app": pref.in_app_enabled,
                "email": pref.email_enabled,
                "sms": pref.sms_enabled,
                "push": pref.push_enabled,
            }
            return channel_map.get(channel, True)
        except NotificationPreference.DoesNotExist:
            return True  # default allow

    def _resolve_batch_targets(self, batch: NotificationBatch) -> list[int]:
        ids = set(batch.target_user_ids or [])
        if batch.target_roles:
            role_ids = User.objects.filter(
                groups__name__in=batch.target_roles, is_active=True
            ).values_list("id", flat=True)
            ids.update(role_ids)
        return list(ids)


# Singleton instance
notification_service = NotificationService()
