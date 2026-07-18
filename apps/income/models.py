from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):

    CATEGORY_CHOICES = [
        ("Salary", "Salary"),
        ("Business", "Business"),
        ("Freelancing", "Freelancing"),
        ("Investment", "Investment"),
        ("Rental", "Rental"),
        ("Gift", "Gift"),
        ("Other", "Other"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
        ("Debit Card", "Debit Card"),
        ("Credit Card", "Credit Card"),
        ("Cheque", "Cheque"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incomes"
    )

    title = models.CharField(
        max_length=100
    )

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
        choices=PAYMENT_METHOD_CHOICES
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-date"]

        verbose_name = "Income"

        verbose_name_plural = "Income Records"

    def __str__(self):

        return f"{self.title} - ₹{self.amount}"