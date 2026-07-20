from datetime import date

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render

from apps.budgets.models import Budget
from apps.expense.models import Expense
from apps.income.models import Income

from .forms import (
    RegisterForm,
    LoginForm,
    EditProfileForm,
    CustomPasswordChangeForm,
)


def landing_view(request):
    return render(request, "accounts/landing.html")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            User.objects.create_user(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            messages.success(request, "Registration Successful!")

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            user = form.cleaned_data["user"]

            login(request, user)

            messages.success(
                request,
                "Login Successful."
            )

            return redirect("dashboard")

    else:

        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged Out Successfully."
    )

    return redirect("landing")


# ==========================
# Dashboard
# ==========================

@login_required(login_url="login")
def dashboard_view(request):

    incomes = Income.objects.filter(
        user=request.user
    ).order_by("-date")

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    balance = total_income - total_expense

    today = date.today()

    current_budget = Budget.objects.filter(
        user=request.user,
        month=today.month,
        year=today.year,
    ).first()

    context = {

        "total_income": total_income,

        "total_expense": total_expense,

        "balance": balance,

        "current_budget": (
            current_budget.amount
            if current_budget
            else 0
        ),

        "income_count": incomes.count(),

        "expense_count": expenses.count(),

        "recent_incomes": incomes[:5],

        "recent_expenses": expenses[:5],

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


# ==========================
# Profile
# ==========================

@login_required(login_url="login")
def profile_view(request):

    context = {

        "user_data": request.user

    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )


@login_required(login_url="login")
def edit_profile_view(request):

    if request.method == "POST":

        form = EditProfileForm(
            request.POST,
            instance=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = EditProfileForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form
        }
    )


@login_required(login_url="login")
def change_password_view(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form
        }
    )