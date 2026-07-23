from django.urls import path
from . import views

urlpatterns = [
    path("", views.report_dashboard, name="reports"),
    path("pdf/", views.export_report_pdf, name="export_report_pdf"),
]