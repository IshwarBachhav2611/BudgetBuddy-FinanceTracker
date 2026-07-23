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
from apps.notifications.utils import create_notification


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
            create_notification(
                user,
                "Welcome to BudgetBuddy 🎉",
                "Start tracking your income and expenses today."
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
            create_notification(
                user,
                "Login Successful",
                "Welcome back to BudgetBuddy.",
                "info",
            )

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

    today = date.today()

    # ---------------------------------
    # All Income & Expense Records
    # ---------------------------------

    incomes = Income.objects.filter(
        user=request.user
    ).order_by("-date")

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")

    # ---------------------------------
    # Overall Totals
    # ---------------------------------

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0
    

    total_savings = total_income - total_expense

    # ---------------------------------
    # Current Month Income
    # ---------------------------------

    month_income = Income.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year,
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # ---------------------------------
    # Current Month Expense
    # ---------------------------------

    month_expense = Expense.objects.filter(
        user=request.user,
        date__month=today.month,
        date__year=today.year,
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # ---------------------------------
    # Current Month Budget
    # ---------------------------------

    current_budget = Budget.objects.filter(
        user=request.user,
        month=today.month,
        year=today.year,
    ).first()

    budget_amount = current_budget.amount if current_budget else 0

    # ---------------------------------
    # Current Month Balance
    # ---------------------------------

    month_balance = month_income - month_expense

    # ---------------------------------
    # Budget Alert
    # ---------------------------------

    alert_message = None
    alert_type = None

    if budget_amount > 0:

        usage = (month_expense / budget_amount) * 100

        if month_expense > budget_amount:

            extra = month_expense - budget_amount

            alert_type = "danger"

            alert_message = (
                f"You have exceeded this month's budget by ₹ {extra:.2f}."
            )
            create_notification(
                request.user,
                "Budget Exceeded",
                alert_message,
                "danger",
            )

        elif usage >= 85:

            remaining = budget_amount - month_expense

            alert_type = "warning"

            alert_message = (
                f"You have used {usage:.0f}% of your budget. "
                f"Only ₹ {remaining:.2f} remaining."
            )
            create_notification(
                request.user,
                "Budget Warning",
                alert_message,
                "warning",
            )

        else:

            remaining = budget_amount - month_expense

            alert_type = "success"

            alert_message = (
                f"Great! You are within budget. "
                f"₹ {remaining:.2f} remaining this month."
            )

    # ---------------------------------
    # Context
    # ---------------------------------

    context = {

        # Current Month

        "month_income": month_income,
        "month_expense": month_expense,
        "current_budget": budget_amount,
        "month_balance": month_balance,

        # Overall

        "total_income": total_income,
        "total_expense": total_expense,
        "total_savings": total_savings,

        # Counts

        "income_count": incomes.count(),
        "expense_count": expenses.count(),

        # Recent Records

        "recent_incomes": incomes[:5],
        "recent_expenses": expenses[:5],

        # Budget Alert

        "alert_message": alert_message,
        "alert_type": alert_type,
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
            create_notification(
                request.user,
                "Profile Updated",
                "Your profile information has been updated.",
                "success",
            )

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

            create_notification(
                request.user,
                "Password Changed",
                "Your account password was changed successfully.",
                "warning",
            )

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