from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Notification


@login_required
def notification_list(request):

    notifications = Notification.objects.filter(
        user=request.user
    )

    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications
        }
    )


@login_required
def mark_notification_read(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user,
    )

    notification.is_read = True
    notification.save()

    if notification.action_url:
        return redirect(notification.action_url)

    return redirect("notifications")


@login_required
def mark_all_read(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(is_read=True)

    messages.success(
        request,
        "All notifications marked as read."
    )

    return redirect("notifications")


@login_required
def delete_notification(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        user=request.user,
    )

    notification.delete()

    messages.success(
        request,
        "Notification deleted."
    )

    return redirect("notifications")


@login_required
def clear_notifications(request):

    Notification.objects.filter(
        user=request.user
    ).delete()

    messages.success(
        request,
        "All notifications cleared."
    )

    return redirect("notifications")