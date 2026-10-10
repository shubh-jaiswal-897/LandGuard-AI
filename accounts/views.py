from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or 'dashboard:index'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('accounts:login')


def user_profile_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False})

    profile = getattr(request.user, 'profile', None)
    return JsonResponse({
        'authenticated': True,
        'username': request.user.username,
        'email': request.user.email,
        'role': profile.role if profile else ('ADMINISTRATOR' if request.user.is_superuser else 'VIEWER'),
        'role_display': profile.get_role_display() if profile else ('Administrator' if request.user.is_superuser else 'Viewer'),
        'department': profile.department if profile else 'Ministry of Infrastructure'
    })
