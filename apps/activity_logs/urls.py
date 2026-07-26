from django.urls import path
from . import views

urlpatterns = [
    path("", views.activity_list, name="activity_logs"),
    path("admin/", views.admin_activity_list, name="admin_activity_logs"),
]