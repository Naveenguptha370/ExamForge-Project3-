from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.DashboardSummaryView.as_view(), name="analytics-dashboard"),
    path("snapshots/", views.SnapshotListView.as_view(), name="analytics-snapshots"),
    path("snapshots/record/", views.RecordSnapshotView.as_view(), name="analytics-record-snapshot"),
    path("trends/", views.TrendView.as_view(), name="analytics-trends"),
    path("departments/", views.DepartmentMetricView.as_view(), name="analytics-departments"),
    path("health/", views.SystemHealthView.as_view(), name="analytics-health"),
    path("activity/", views.UserActivityView.as_view(), name="analytics-activity"),
]
