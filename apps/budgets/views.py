from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BudgetForm
from .models import Budget
from datetime import date
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from apps.notifications.utils import create_notification
from calendar import month_name
from apps.activity_logger import log_activity

@login_required
def budget_list(request):

    # Get all budgets ordered by latest year/month
    budget_records = Budget.objects.filter(
        user=request.user
    ).order_by("-year", "-month")

    # Create available months for dropdown
    available_months = []

    for budget in budget_records:

        month_date = date(
            budget.year,
            budget.month,
            1,
        )

        if month_date not in available_months:
            available_months.append(month_date)

    # No budgets available
    if not available_months:

        return render(
            request,
            "budgets/budget_list.html",
            {
                "budgets": [],
                "total_budget": 0,
                "available_months": [],
                "selected_month": None,
            },
        )

    # Selected month
    selected = request.GET.get("month")

    if selected:

        selected_month = date.fromisoformat(
            selected + "-01"
        )

    else:

        selected_month = available_months[0]

    # Filter budgets
    budgets = Budget.objects.filter(
        user=request.user,
        year=selected_month.year,
        month=selected_month.month,
    ).order_by("-year", "-month")

    # Total Budget
    total_budget = budgets.aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {

        "budgets": budgets,

        "total_budget": total_budget,

        "available_months": available_months,

        "selected_month": selected_month,

    }

    return render(
        request,
        "budgets/budget_list.html",
        context,
    )

@login_required
def add_budget(request):

    if request.method == "POST":

        form = BudgetForm(request.POST)

        if form.is_valid():

            budget = form.save(commit=False)

            budget.user = request.user

            existing_budget = Budget.objects.filter(
                user=request.user,
                month=budget.month,
                year=budget.year,
            ).exists()

            if existing_budget:
                messages.warning(
                    request,
                    f"A budget for {month_name[budget.month]} {budget.year} already exists. Please edit the existing budget."
                )
                return render(
                    request,
                    "budgets/add_budget.html",
                    {"form": form},
                )

            budget.save()

            log_activity(
                request.user,
                "Budget Created",
                {
                    "amount": float(budget.amount),
                    "month": budget.month,
                    "year": budget.year,
                }
            )

            create_notification(
                request.user,
                "Budget Created",
                f"Monthly budget of ₹{budget.amount} has been created.",
                "success",
            )

            messages.success(
                request,
                "Budget created successfully!"
            )

            return redirect("budget_list")

    else:

        form = BudgetForm()

    return render(
        request,
        "budgets/add_budget.html",
        {
            "form": form
        }
    )


@login_required
def edit_budget(request, id):

    budget = get_object_or_404(
        Budget,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = BudgetForm(
            request.POST,
            instance=budget
        )

        if form.is_valid():

            form.save()

            log_activity(
                request.user,
                "Budget Updated",
                {
                    "amount": float(budget.amount),
                    "month": budget.month,
                    "year": budget.year,
                }
            )

            create_notification(
                request.user,
                "Budget Updated",
                f"Budget updated to ₹{budget.amount}.",
                "info",
            )
            
            messages.success(
                request,
                "Budget updated successfully!"
            )

            return redirect("budget_list")

    else:

        form = BudgetForm(instance=budget)

    return render(
        request,
        "budgets/edit_budget.html",
        {
            "form": form
        }
    )


@login_required
def delete_budget(request, id):

    budget = get_object_or_404(
        Budget,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        amount = budget.amount
        month = budget.month
        year = budget.year

        budget.delete()

        log_activity(
            request.user,
            "Budget Deleted",
            {
                "amount": float(amount),
                "month": month,
                "year": year,
            }
        )

        create_notification(
            request.user,
            "Budget Deleted",
            f"Budget of ₹{amount} was deleted.",
            "danger",
        )

        messages.success(
            request,
            "Budget deleted successfully!"
        )

        return redirect("budget_list")

    return render(
        request,
        "budgets/delete_budget.html",
        {
            "budget": budget
        }
    )