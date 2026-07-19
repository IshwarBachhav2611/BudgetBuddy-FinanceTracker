from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "amount",
        "category",
        "payment_method",
        "date",
        "user",
    )

    list_filter = (
        "category",
        "payment_method",
    )

    search_fields = (
        "title",
    )