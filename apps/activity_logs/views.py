from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from apps.mongodb import activity_logs


@login_required
def activity_list(request):
    activities = list(
        activity_logs.find(
            {"user_id": request.user.id}
        ).sort("created_at", -1)
    )

    return render(
        request,
        "activity_logs/activity_list.html",
        {"activities": activities},
    )


@user_passes_test(lambda u: u.is_superuser)
def admin_activity_list(request):
    activities = list(
        activity_logs.find().sort("created_at", -1).limit(200)
    )

    return render(
        request,
        "activity_logs/admin_activity_list.html",
        {"activities": activities},
    )