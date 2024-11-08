from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import FarmerProfile, CustomerProfile
from product_app.models import Product

def HomePage(request):
    return render(request, 'HomePage.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        role = request.POST.get('role')

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create the correct profile based on role
                if role == 'farmer':
                    FarmerProfile.objects.create(user=user)
                else:
                    CustomerProfile.objects.create(user=user)

                messages.success(request, "Registration successful! You can log in now.")
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Registration error: {e}")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check user profile type and redirect accordingly
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            elif FarmerProfile.objects.filter(user=user).exists():
                return redirect('farmer_dashboard')
            elif CustomerProfile.objects.filter(user=user).exists():
                return redirect('customer_dashboard')
            else:
                messages.error(request, "Profile not found.")
                return redirect('HomePage')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('HomePage')
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

