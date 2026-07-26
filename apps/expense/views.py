from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ExpenseForm
from .models import Expense
from datetime import date
from django.db.models.functions import TruncMonth
from apps.notifications.utils import create_notification
from apps.activity_logger import log_activity

@login_required
def expense_list(request):

    available_months = (
        Expense.objects.filter(user=request.user)
        .annotate(month_date=TruncMonth("date"))
        .values_list("month_date", flat=True)
        .distinct()
        .order_by("-month_date")
    )

    available_months = list(available_months)

    if len(available_months) == 0:

        return render(
            request,
            "expense/expense_list.html",
            {
                "expenses": [],
                "total_expense": 0,
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

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=selected_month.year,
        date__month=selected_month.month,
    ).order_by("-date")

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {

        "expenses": expenses,

        "total_expense": total_expense,

        "total_transactions": expenses.count(),

        "available_months": available_months,

        "selected_month": selected_month,

    }

    return render(
        request,
        "expense/expense_list.html",
        context,
    )

@login_required
def add_expense(request):

    if request.method == "POST":

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)
            expense.user = request.user

            expense.save()

            log_activity(
                request.user,
                "Expense Added",
                {
                    "title": expense.title,
                    "amount": float(expense.amount),
                    "category": expense.category,
                    "payment_method": expense.payment_method,
                    "date": str(expense.date),
                }
            )

            create_notification(
                request.user,
                "Expense Added",
                f"₹{expense.amount} spent on {expense.category}.",
                "warning",
                "/expense/",
            )
            
            messages.success(request, "Expense added successfully!")

            return redirect("expense_list")

        else:
            print(form.errors)   # Shows errors in terminal

    else:

        form = ExpenseForm()

    return render(
        request,
        "expense/add_expense.html",
        {
            "form": form
        }
    )

@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            log_activity(
                request.user,
                "Expense Updated",
                {
                    "title": expense.title,
                    "amount": float(expense.amount),
                    "category": expense.category,
                    "payment_method": expense.payment_method,
                    "date": str(expense.date),
                }
            )

            create_notification(
                request.user,
                "Expense Updated",
                f"{expense.category} expense was updated.",
                "info",
                "/expense/",
            )

            messages.success(
                request,
                "Expense updated successfully!"
            )

            return redirect("expense_list")

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(
        request,
        "expense/edit_expense.html",
        {
            "form": form
        }
    )


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        category = expense.category
        amount = expense.amount

        expense.delete()

        log_activity(
            request.user,
            "Expense Deleted",
            {
                "title": expense.title,
                "amount": float(expense.amount),
                "category": expense.category,
                "payment_method": expense.payment_method,
                "date": str(expense.date),
            }
        )

        create_notification(
            request.user,
            "Expense Deleted",
            f"₹{amount} expense from {category} was deleted.",
            "danger",
            "/expense/",
        )
        
        messages.success(
            request,
            "Expense deleted successfully!"
        )

        return redirect("expense_list")

    return render(
        request,
        "expense/delete_expense.html",
        {
            "expense": expense
        }
    )