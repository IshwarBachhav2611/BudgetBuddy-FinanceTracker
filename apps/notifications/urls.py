from django.urls import path
from . import views

urlpatterns = [

    # Notification List
    path(
        "",
        views.notification_list,
        name="notifications",
    ),

    # Mark One Notification Read
    path(
        "<int:id>/read/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),

    # Mark All Read
    path(
        "mark-all-read/",
        views.mark_all_read,
        name="mark_all_read",
    ),

    # Delete One Notification
    path(
        "<int:id>/delete/",
        views.delete_notification,
        name="delete_notification",
    ),

    # Clear All Notifications
    path(
        "clear/",
        views.clear_notifications,
        name="clear_notifications",
    ),
]