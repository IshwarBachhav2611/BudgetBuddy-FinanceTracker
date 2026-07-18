from django.urls import path

from . import views

urlpatterns = [

    path("", views.landing_view, name="landing"),

    path("register/", views.register_view, name="register"),

    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_view, name="dashboard"),

    path("profile/", views.profile_view, name="profile"),

    path("edit-profile/", views.edit_profile_view, name="edit_profile"),

    path("change-password/", views.change_password_view, name="change_password"),

]