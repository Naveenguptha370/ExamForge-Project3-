from django.urls import path
from . import views

urlpatterns = [
    path("", views.NotificationListView.as_view(), name="notification-list"),
    path("unread-count/", views.NotificationUnreadCountView.as_view(), name="notification-unread-count"),
    path("read-all/", views.NotificationMarkAllReadView.as_view(), name="notification-read-all"),
    path("archive/", views.NotificationArchiveView.as_view(), name="notification-archive"),
    path("preferences/", views.NotificationPreferenceView.as_view(), name="notification-preferences"),
    path("preferences/update/", views.NotificationPreferenceUpdateView.as_view(), name="notification-preferences-update"),
    path("stats/", views.NotificationStatsView.as_view(), name="notification-stats"),
    path("<uuid:pk>/", views.NotificationDetailView.as_view(), name="notification-detail"),
    path("<uuid:pk>/read/", views.NotificationMarkReadView.as_view(), name="notification-mark-read"),
    path("admin/batches/", views.BatchListCreateView.as_view(), name="notification-batch-list"),
    path("admin/batches/<uuid:pk>/dispatch/", views.BatchDispatchView.as_view(), name="notification-batch-dispatch"),
]
