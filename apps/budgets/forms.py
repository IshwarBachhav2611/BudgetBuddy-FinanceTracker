from django import forms
from .models import Budget


class BudgetForm(forms.ModelForm):

    class Meta:

        model = Budget

        fields = [
            "amount",
            "month",
            "year",
        ]

        widgets = {

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Monthly Budget"
                }
            ),

            "month": forms.Select(
                choices=[
                    (1, "January"),
                    (2, "February"),
                    (3, "March"),
                    (4, "April"),
                    (5, "May"),
                    (6, "June"),
                    (7, "July"),
                    (8, "August"),
                    (9, "September"),
                    (10, "October"),
                    (11, "November"),
                    (12, "December"),
                ],
                attrs={
                    "class": "form-select"
                }
            ),

            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2026"
                }
            ),

        }