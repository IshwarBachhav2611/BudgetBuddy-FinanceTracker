from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Transport", "Transport"),
        ("Shopping", "Shopping"),
        ("Bills", "Bills"),
        ("Entertainment", "Entertainment"),
        ("Healthcare", "Healthcare"),
        ("Education", "Education"),
        ("Travel", "Travel"),
        ("Rent", "Rent"),
        ("Other", "Other"),
    ]

    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("UPI", "UPI"),
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_CHOICES
    )

    date = models.DateField()

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title