from .forms import IncomeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Income
from django.shortcuts import get_object_or_404, redirect, render

from datetime import date
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from apps.notifications.utils import create_notification

from apps.activity_logger import log_activity

@login_required
def income_list(request):

    available_months = (
        Income.objects.filter(user=request.user)
        .annotate(month_date=TruncMonth("date"))
        .values_list("month_date", flat=True)
        .distinct()
        .order_by("-month_date")
    )

    available_months = list(available_months)

    if len(available_months) == 0:

        return render(
            request,
            "income/income_list.html",
            {
                "incomes": [],
                "total_income": 0,
                "total_transactions": 0,
                "available_months": [],
                "selected_month": None,
            },
        )

    selected = request.GET.get("month")

    if selected:
        selected_month = date.fromisoformat(selected + "-01")
    else:
        selected_month = available_months[0]

    incomes = Income.objects.filter(
        user=request.user,
        date__year=selected_month.year,
        date__month=selected_month.month,
    ).order_by("-date")

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "income/income_list.html",
        {
            "incomes": incomes,
            "total_income": total_income,
            "total_transactions": incomes.count(),
            "available_months": available_months,
            "selected_month": selected_month,
        },
    )



@login_required
def add_income(request):

    if request.method == "POST":

        form = IncomeForm(request.POST)

        if form.is_valid():

            income = form.save(commit=False)

            income.user = request.user

            income.save()
            log_activity(
                request.user,
                "Income Added",
                {
                    "title": income.title,
                    "category": income.category,
                    "amount": float(income.amount),
                    "date": str(income.date),
                }
            )

            create_notification(
                request.user,
                "Income Added",
                f"₹{income.amount} added for '{income.title}'.",
                "success",
            )
 
            messages.success(request, "Income added successfully!")

            return redirect("income_list")

    else:

        form = IncomeForm()

    return render(
        request, "income/add_income.html",
        {
            "form": form
        }
    )


@login_required
def edit_income(request, id):

    income = get_object_or_404(
        Income,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = IncomeForm(
            request.POST,
            instance=income
        )

        if form.is_valid():

            form.save()

            log_activity(
                request.user,
                "Income Updated",
                {
                    "title": income.title,
                    "category": income.category,
                    "amount": float(income.amount),
                    "date": str(income.date),
                }
            )

            create_notification(
                request.user,
                "Income Updated",
                f"'{income.title}' income was updated.",
                "info",
            )
            messages.success(
                request,
                "Income updated successfully!"
            )

            return redirect("income_list")

    else:

        form = IncomeForm(
            instance=income
        )

    return render(
        request,
        "income/edit_income.html",
        {
            "form": form
        }
    )

@login_required
def delete_income(request, id):

    income = get_object_or_404(
        Income,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        title = income.title
        category = income.category
        amount = income.amount

        income.delete()

        log_activity(
            request.user,
            "Income Deleted",
            {
                "title": title,
                "category": category,
                "amount": float(amount),
            }
        )

        create_notification(
            request.user,
            "Income Deleted",
            f"₹{amount} from '{title}' was deleted.",
            "danger",
        )

        messages.success(
            request,
            "Income deleted successfully!"
        )

        return redirect("income_list")

    return render(
        request,
        "income/delete_income.html",
        {
            "income": income
        }
    )