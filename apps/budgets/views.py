from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BudgetForm
from .models import Budget


@login_required
def budget_list(request):

    budgets = Budget.objects.filter(
        user=request.user
    ).order_by("-year", "-month")

    context = {
        "budgets": budgets
    }

    return render(
        request,
        "budgets/budget_list.html",
        context
    )


@login_required
def add_budget(request):

    if request.method == "POST":

        form = BudgetForm(request.POST)

        if form.is_valid():

            budget = form.save(commit=False)

            budget.user = request.user

            budget.save()

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

        budget.delete()

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