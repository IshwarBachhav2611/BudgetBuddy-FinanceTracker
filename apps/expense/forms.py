from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:

        model = Expense

        fields = [
            "title",
            "amount",
            "category",
            "payment_method",
            "date",
            "description",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter expense title"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter amount"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter description (optional)"
                }
            ),
        }