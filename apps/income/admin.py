from django.contrib import admin
from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "amount",
        "category",
        "payment_method",
        "date",
        "user",
    )

    search_fields = (
        "title",
        "category",
        "user__username",
    )

    list_filter = (
        "category",
        "payment_method",
        "date",
    )

    ordering = ("-date",)