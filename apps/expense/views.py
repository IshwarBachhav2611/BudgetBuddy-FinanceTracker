from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {
        "expenses": expenses,
        "total_expense": total_expense,
        "total_transactions": expenses.count(),
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

        expense.delete()

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