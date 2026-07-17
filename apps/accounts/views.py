from django.shortcuts import render

def landing_view(request):

    return render(request, 'accounts/landing.html')

def register_view(request):

    return render(request, 'accounts/register.html')

def login_view(request):

    return render(request, 'accounts/login.html')

def profile_view(request):

    return render(request, 'accounts/profile.html')

def edit_profile_view(request):

    return render(request, 'accounts/edit_profile.html')

def change_password_view(request):

    return render(request, 'accounts/change_password.html')
