from django.urls import path

from .views import (
    IncomeListCreateApi,
    IncomeDetailApi,

    ExpenseListCreateApi,
    ExpenseDetailApi,

    BudgetListCreateApi,
    BudgetDetailApi,

    NotificationListApi,
    NotificationDetailApi,
    NotificationMarkReadApi,
    NotificationMarkAllReadApi,
    NotificationDeleteApi,
    NotificationClearApi,

    DashboardReportApi,
)

urlpatterns = [

    # Income

    path(
        "income/",
        IncomeListCreateApi.as_view(),
        name="income-api",
    ),

    path(
        "income/<int:pk>/",
        IncomeDetailApi.as_view(),
        name="income-detail-api",
    ),

    # Expense

    path(
        "expense/",
        ExpenseListCreateApi.as_view(),
        name="expense-api",
    ),

    path(
        "expense/<int:pk>/",
        ExpenseDetailApi.as_view(),
        name="expense-detail-api",
    ),

    # Budget

    path(
        "budget/",
        BudgetListCreateApi.as_view(),
        name="budget-api",
    ),

    path(
        "budget/<int:pk>/",
        BudgetDetailApi.as_view(),
        name="budget-detail-api",
    ),

    # Notifications

    path(
        "notifications/",
        NotificationListApi.as_view(),
        name="notification-api",
    ),

    path(
        "notifications/<int:pk>/",
        NotificationDetailApi.as_view(),
        name="notification-detail-api",
    ),

    path(
        "notifications/<int:pk>/read/",
        NotificationMarkReadApi.as_view(),
        name="notification-read-api",
    ),

    path(
        "notifications/mark-all-read/",
        NotificationMarkAllReadApi.as_view(),
        name="notification-mark-all-read-api",
    ),

    path(
        "notifications/<int:pk>/delete/",
        NotificationDeleteApi.as_view(),
        name="notification-delete-api",
    ),

    path(
        "notifications/clear/",
        NotificationClearApi.as_view(),
        name="notification-clear-api",
    ),

    path(
        "reports/dashboard/",
        DashboardReportApi.as_view(),
        name="dashboard-report-api",
    ),
]