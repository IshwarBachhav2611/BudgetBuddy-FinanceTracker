from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.income.models import Income
from apps.expense.models import Expense

from apps.budgets.models import Budget
from .serializers import BudgetSerializer

from apps.notifications.models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from datetime import date


from .serializers import (
    IncomeSerializer,
    ExpenseSerializer,
)


# ----------------------------
# Income API
# ----------------------------

class IncomeListCreateApi(generics.ListCreateAPIView):

    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeDetailApi(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


# ----------------------------
# Expense API
# ----------------------------

class ExpenseListCreateApi(generics.ListCreateAPIView):

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailApi(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


# ----------------------------
# Budget API
# ----------------------------

class BudgetListCreateApi(generics.ListCreateAPIView):

    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetDetailApi(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


# ----------------------------
# Notification API
# ----------------------------

class NotificationListApi(generics.ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

class NotificationDetailApi(generics.RetrieveAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

class NotificationMarkReadApi(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        notification = Notification.objects.get(
            pk=pk,
            user=request.user,
        )

        notification.is_read = True
        notification.save()

        return Response({
            "message": "Notification marked as read."
        })

class NotificationMarkAllReadApi(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True)

        return Response({
            "message": "All notifications marked as read."
        })

class NotificationDeleteApi(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

class NotificationClearApi(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        Notification.objects.filter(
            user=request.user
        ).delete()

        return Response({
            "message": "All notifications deleted."
        })

class DashboardReportApi(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = date.today()

        total_income = (
            Income.objects.filter(user=request.user)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        total_expense = (
            Expense.objects.filter(user=request.user)
            .aggregate(total=Sum("amount"))["total"] or 0
        )

        month_income = (
            Income.objects.filter(
                user=request.user,
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum("amount"))["total"] or 0
        )

        month_expense = (
            Expense.objects.filter(
                user=request.user,
                date__month=today.month,
                date__year=today.year,
            ).aggregate(total=Sum("amount"))["total"] or 0
        )

        budget = Budget.objects.filter(
            user=request.user,
            month=today.month,
            year=today.year,
        ).first()

        budget_amount = budget.amount if budget else 0

        data = {
            "total_income": total_income,
            "total_expense": total_expense,
            "total_savings": total_income - total_expense,
            "month_income": month_income,
            "month_expense": month_expense,
            "current_budget": budget_amount,
            "month_balance": month_income - month_expense,
            "income_count": Income.objects.filter(user=request.user).count(),
            "expense_count": Expense.objects.filter(user=request.user).count(),
        }

        return Response(data)