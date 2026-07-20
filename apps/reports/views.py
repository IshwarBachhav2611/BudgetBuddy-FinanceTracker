from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def report_dashboard(request):
    return render(
        request,
        "reports/report_dashboard.html",
    )