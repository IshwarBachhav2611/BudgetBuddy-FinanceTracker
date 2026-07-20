from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    month = models.PositiveSmallIntegerField()

    year = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-year", "-month"]

        unique_together = ("user", "month", "year")

    def __str__(self):

        return f"{self.month}/{self.year} - ₹{self.amount}"