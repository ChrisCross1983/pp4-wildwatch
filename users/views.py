from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.

# Registration View

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('users:login')
        else:
            # Debugging
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')