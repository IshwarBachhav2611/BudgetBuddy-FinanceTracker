from django.urls import path
from . import views

urlpatterns = [

    path("", views.income_list, name="income_list"),

    path("add/", views.add_income, name="add_income"),

    path("edit/<int:id>/", views.edit_income, name="edit_income"),

    path("delete/<int:id>/", views.delete_income, name="delete_income"),
    

]