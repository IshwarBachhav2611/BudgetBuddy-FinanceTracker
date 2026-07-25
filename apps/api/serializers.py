from rest_framework import serializers

from apps.income.models import Income
from apps.expense.models import Expense
from apps.budgets.models import Budget
from apps.notifications.models import Notification


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
            "updated_at",
        ]

