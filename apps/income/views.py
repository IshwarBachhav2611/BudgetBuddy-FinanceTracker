from .forms import IncomeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Income
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def income_list(request):

    incomes = Income.objects.filter(
        user=request.user
    ).order_by("-date")

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {

        "incomes": incomes,

        "total_income": total_income,

        "total_transactions": incomes.count(),

    }

    return render(
        request,
        "income/income_list.html",
        context
    )


@login_required
def add_income(request):

    if request.method == "POST":

        form = IncomeForm(request.POST)

        if form.is_valid():

            income = form.save(commit=False)

            income.user = request.user

            income.save()

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

        income.delete()

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