from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.db.models.functions import TruncMonth, ExtractYear, ExtractMonth
from apps.income.models import Income
from apps.expense.models import Expense
from apps.budgets.models import Budget
from django.db.models import Sum, Count
import json
from django.http import HttpResponse
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


@login_required
def report_dashboard(request):

    today = date.today()

    report_type = request.GET.get("type", "monthly")
    month = int(request.GET.get("month", today.month))
    year = int(request.GET.get("year", today.year))

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    # -------------------------
    # Available Years
    # -------------------------

    income_years = incomes.dates("date", "year")
    expense_years = expenses.dates("date", "year")

    years = sorted(
        set(
            [d.year for d in income_years] +
            [d.year for d in expense_years]
        ),
        reverse=True
    )

    if not years:
        years = [today.year]

    # -------------------------
    # Monthly Report
    # -------------------------

    if report_type == "monthly":

        incomes = incomes.filter(
            date__month=month,
            date__year=year
        )

        expenses = expenses.filter(
            date__month=month,
            date__year=year
        )

        budgets = budgets.filter(
            month=month,
            year=year
        )

    # -------------------------
    # Yearly Report
    # -------------------------

    elif report_type == "yearly":

        incomes = incomes.filter(date__year=year)
        expenses = expenses.filter(date__year=year)
        budgets = budgets.filter(year=year)

    # -------------------------
    # Totals
    # -------------------------

    income = incomes.aggregate(total=Sum("amount"))["total"] or 0
    expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
    budget = budgets.aggregate(total=Sum("amount"))["total"] or 0
    savings = income - expense
    
    expense_categories = (
    expenses.values("category")
    .annotate(total=Sum("amount"))
    .order_by("-total")
    )

    expense_labels = []
    expense_values = []

    for item in expense_categories:

        expense_labels.append(item["category"])
        expense_values.append(float(item["total"]))

    available_months = (
        Income.objects.filter(user=request.user)
        .annotate(month_date=TruncMonth("date"))
        .values_list("month_date", flat=True)
        .distinct()
        .order_by("-month_date")
    )

    # ===========================
    # Income vs Expense Bar Chart
    # ===========================

    chart_income = income
    chart_expense = expense
    chart_savings = savings


    # ======================================
    # Monthly Financial Trend (12 Months)
    # ======================================

    income_trend = [0] * 12
    expense_trend = [0] * 12

    # Income totals by month
    income_months = (
        incomes.values(month=ExtractMonth("date"))
        .annotate(total=Sum("amount"))
    )

    for item in income_months:
        income_trend[item["month"] - 1] = float(item["total"])

    # Expense totals by month
    expense_months = (
        expenses.values(month=ExtractMonth("date"))
        .annotate(total=Sum("amount"))
    )

    for item in expense_months:
        expense_trend[item["month"] - 1] = float(item["total"])

    # Savings = Income - Expense
    saving_trend = []

    for i in range(12):
        saving_trend.append(
            income_trend[i] - expense_trend[i]
        )

    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    context = {

        "report_type": report_type,

        "selected_month": month,
        "selected_year": year,

        "available_years": years,

        "report_income": income,
        "report_expense": expense,
        "report_budget": budget,
        "report_savings": savings,

        "available_months": available_months,

        # Chart Data
        "chart_income": float(income),
        "chart_expense": float(expense),
        "chart_savings": float(savings),

        "expense_labels": expense_labels,
        "expense_values": expense_values,

        "chart_income": chart_income,
        "chart_expense": chart_expense,
        "chart_savings": chart_savings,

        "months": json.dumps(months),

        "income_trend": json.dumps(income_trend),

        "expense_trend": json.dumps(expense_trend),

        "saving_trend": json.dumps(saving_trend),

    }

    return render(
        request,
        "reports/reports.html",
        context,
    )

@login_required
def export_report_pdf(request):

    today = date.today()

    report_type = request.GET.get(
        "type",
        "monthly"
    )

    month = int(
        request.GET.get(
            "month",
            today.month
        )
    )

    year = int(
        request.GET.get(
            "year",
            today.year
        )
    )

    incomes = Income.objects.filter(
        user=request.user
    )

    expenses = Expense.objects.filter(
        user=request.user
    )

    budgets = Budget.objects.filter(
        user=request.user
    )

    if report_type == "monthly":

        incomes = incomes.filter(
            date__month=month,
            date__year=year
        )

        expenses = expenses.filter(
            date__month=month,
            date__year=year
        )

        budgets = budgets.filter(
            month=month,
            year=year
        )

    elif report_type == "yearly":

        incomes = incomes.filter(
            date__year=year
        )

        expenses = expenses.filter(
            date__year=year
        )

        budgets = budgets.filter(
            year=year
        )

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_budget = budgets.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_savings = total_income - total_expense

    income_summary = (
        incomes.values("category")
        .annotate(
            total=Sum("amount"),
            count=Count("id")
        )
        .order_by("category")
    )

    expense_summary = (
        expenses.values("category")
        .annotate(
            total=Sum("amount"),
            count=Count("id")
        )
        .order_by("category")
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="Budget_Report.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setTitle("BudgetBuddy Report")

    # -----------------------------
    # Report Title
    # -----------------------------

    pdf.setFillColor(HexColor("#0d6efd"))
    pdf.setFont("Helvetica-Bold", 28)

    pdf.drawCentredString(
        300,
        800,
        "BudgetBuddy"
    )

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawCentredString(
        300,
        775,
        "Personal Finance Report"
    )

    pdf.line(60, 760, 540, 760)

    # -----------------------------
    # Report Details
    # -----------------------------

    pdf.setFillColor(HexColor("#000000"))

    pdf.setFont("Helvetica-Bold", 13)

    pdf.drawString(70, 725, "Prepared For")
    pdf.drawString(70, 700, "Report Type")
    pdf.drawString(70, 675, "Reporting Period")
    pdf.drawString(70, 650, "Generated On")
    pdf.drawString(70, 625, "Application")

    pdf.setFont("Helvetica", 13)

    pdf.drawString(220, 725, request.user.username)

    pdf.drawString(
        220,
        700,
        report_type.title()
    )

    if report_type == "monthly":

        period = date(year, month, 1).strftime("%B %Y")

    elif report_type == "yearly":

        period = str(year)

    else:

        period = "All Time"

    pdf.drawString(
        220,
        675,
        period
    )

    pdf.drawString(
        220,
        650,
        date.today().strftime("%d %B %Y")
    )

    pdf.drawString(
        220,
        625,
        "BudgetBuddy v1.0"
    )

    pdf.line(60, 605, 540, 605)


    # ---------------------------------------
    # Financial Summary
    # ---------------------------------------

    y = 565

    pdf.setFillColor(HexColor("#0d6efd"))
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Financial Summary")

    y -= 15

    pdf.setStrokeColor(HexColor("#cccccc"))
    pdf.line(50, y, 550, y)

    y -= 30

    pdf.setFillColor(HexColor("#000000"))
    pdf.setFont("Helvetica", 12)

    pdf.drawString(60, y, "Total Income")
    pdf.drawRightString(520, y, f"Rs. {total_income:,.2f}")

    y -= 25

    pdf.drawString(60, y, "Total Expense")
    pdf.drawRightString(520, y, f"Rs. {total_expense:,.2f}")

    y -= 25

    pdf.drawString(60, y, "Total Budget")
    pdf.drawRightString(520, y, f"Rs. {total_budget:,.2f}")

    y -= 25

    pdf.drawString(60, y, "Total Savings")
    pdf.drawRightString(520, y, f"Rs. {total_savings:,.2f}")

    y -= 20

    pdf.line(50, y, 550, y)

    y -= 35

    if report_type == "monthly":
        # ---------------------------------------
        # Income Transactions
        # ---------------------------------------

        # Start below Financial Summary

        pdf.setFillColor(HexColor("#198754"))
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(50, y, "Income Transactions")

        y -= 25

        # Table Header
        pdf.setFillColor(HexColor("#0d6efd"))
        pdf.rect(50, y, 500, 20, fill=1)

        pdf.setFillColor(HexColor("#ffffff"))
        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(55, y + 5, "Date")
        pdf.drawString(130, y + 5, "Title")
        pdf.drawString(280, y + 5, "Category")
        pdf.drawRightString(535, y + 5, "Amount")

        y -= 20

        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(HexColor("#000000"))


        for income in incomes:

            pdf.drawString(
                55,
                y + 5,
                income.date.strftime("%d-%m-%Y")
            )

            pdf.drawString(
                130,
                y + 5,
                income.title[:18]
            )

            pdf.drawString(
                280,
                y + 5,
                income.category
            )

            pdf.drawRightString(
                535,
                y + 5,
                f"Rs. {income.amount}"
            )

            y -= 20

            if y < 80:
                pdf.showPage()
                y = 760

        # ---------------------------------------
        # Expense Transactions
        # ---------------------------------------

        y -= 20

        pdf.setFillColor(HexColor("#dc3545"))
        pdf.setFont("Helvetica-Bold", 15)

        pdf.drawString(
            50,
            y,
            "Expense Transactions"
        )

        y -= 25

        pdf.setFillColor(HexColor("#dc3545"))

        pdf.rect(
            50,
            y,
            500,
            20,
            fill=1
        )

        pdf.setFillColor(HexColor("#ffffff"))

        pdf.setFont(
            "Helvetica-Bold",
            10
        )

        pdf.drawString(55, y + 5, "Date")
        pdf.drawString(120, y + 5, "Title")
        pdf.drawString(235, y + 5, "Category")
        pdf.drawString(355, y + 5, "Payment")
        pdf.drawRightString(535, y + 5, "Amount")

        y -= 20

        pdf.setFillColor(HexColor("#000000"))

        pdf.setFont(
            "Helvetica",
            10
        )

        for expense in expenses:

            pdf.drawString(
                55,
                y + 5,
                expense.date.strftime("%d-%m-%Y")
            )

            pdf.drawString(
                120,
                y + 5,
                expense.title[:15]
            )

            pdf.drawString(
                235,
                y + 5,
                expense.category
            )

            pdf.drawString(
                355,
                y + 5,
                expense.payment_method
            )

            pdf.drawRightString(
                535,
                y + 5,
                f"Rs. {expense.amount}"
            )

            y -= 20

            if y < 80:

                pdf.showPage()

                y = 760

                pdf.setFont("Helvetica", 10)

    else:

        # ---------------------------------------
        # Income Category Summary
        # ---------------------------------------

        pdf.setFillColor(HexColor("#198754"))
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(50, y, "Income Category Summary")

        y -= 25

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(60, y, "Category")
        pdf.drawString(250, y, "Entries")
        pdf.drawRightString(530, y, "Amount")

        y -= 20

        pdf.setFont("Helvetica", 11)

        for item in income_summary:

            pdf.drawString(
                60,
                y,
                item["category"]
            )

            pdf.drawString(
                260,
                y,
                str(item["count"])
            )

            pdf.drawRightString(
                530,
                y,
                f"Rs. {item['total']:,.2f}"
            )

            y -= 20

        # ---------------------------------------
        # Expense Category Summary
        # ---------------------------------------

        y -= 25

        pdf.setFillColor(HexColor("#dc3545"))
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(50, y, "Expense Category Summary")

        y -= 25

        pdf.setFont("Helvetica-Bold", 11)

        pdf.drawString(60, y, "Category")
        pdf.drawString(250, y, "Entries")
        pdf.drawRightString(530, y, "Amount")

        y -= 20

        pdf.setFont("Helvetica", 11)

        for item in expense_summary:

            pdf.drawString(
                60,
                y,
                item["category"]
            )

            pdf.drawString(
                260,
                y,
                str(item["count"])
            )

            pdf.drawRightString(
                530,
                y,
                f"Rs. {item['total']:,.2f}"
            )

            y -= 20

    # ---------------------------------------
    # Footer Note
    # ---------------------------------------

    if y < 60:
        pdf.showPage()
        y = 760

    y -= 20

    pdf.setStrokeColor(HexColor("#d9d9d9"))
    pdf.line(50, y, 550, y)

    y -= 15

    pdf.setFont("Helvetica-Oblique", 9)
    pdf.setFillColor(HexColor("#666666"))

    pdf.drawCentredString(
        300,
        y,
        f"Generated by BudgetBuddy • {date.today().strftime('%d %B %Y')}"
    )

    pdf.save()

    return response