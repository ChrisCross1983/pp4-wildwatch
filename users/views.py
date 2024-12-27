from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomUserUpdateForm, ProfileUpdateForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .utils import send_verification_email
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

# Signup View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_verification_email(user)

            messages.success(
                request,
                "Account created successfully. Please check your email to activate your account.")
            return redirect('users:signup_thanks')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

# Thanks Page after registration
def signup_thanks(request):
    return render(request, 'users/signup_thanks.html')

# Confirm Email
def confirm_email(request, token):
    try:
        profile = Profile.objects.get(email_token=token)

        if profile.user.is_active:
            messages.error(request, "This email is already verified. You can log in.")
            return redirect("users:login")
        
        if profile.email_token_expiry and profile.email_token_expiry < now():
            messages.error(request, "This token has expired. Please request a new confirmation email.")
            return redirect("users:email_confirm_resend")

        profile.user.is_active = True
        profile.email_token = None
        profile.email_token_expiry = None
        profile.user.save()
        profile.save()

        messages.success(request, "Your email has been confirmed! You can now log in.")
        return redirect("users:login")

    except Profile.DoesNotExist:
        messages.error(request, "Invalid token. Please request a new confirmation email.")
        return redirect("users:email_confirm_resend")

# Resend Confirm Email
def email_confirm_resend(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "This email does not exist.")
            return redirect('users:email_confirm_resend')

        if user.is_active:
            messages.error(request, "This email is already verified. Please log in.")
            return redirect('users:login')

        send_verification_email(user)
        messages.success(request, "A new verification email has been sent.")
        return redirect('users:signup_thanks')

    return render(request, 'users/email_confirm_resend.html')

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('home')

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is None:
                form.add_error(None, "Invalid username or password.")
            elif not user.is_active:
                form.add_error(None, "Account is inactive. Please verify your email.")
            else:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
        else:
            logger.error(f"Form invalid: {form.errors}")
    else:
        form = AuthenticationForm()
        logger.debug("GET request to login page")
    return render(request, "users/login.html", {"form": form})

# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('users:home')

# Home View
def home(request):
    context = {'user': request.user} if request.user.is_authenticated else {}
    return render(request, 'users/home.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

# Edit Profile View
@login_required
def edit_profile(request):
    profile = request.user.profile
    old_email = request.user.email

    user_form = CustomUserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=profile)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'save_profile' in request.POST:
            user_form = CustomUserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                new_email = user_form.cleaned_data['email']

                if old_email != new_email:
                    request.user.is_active = False
                    request.user.save()

                    send_verification_email(request.user)
                    messages.success(request, "Your email was updated. Please verify your new email.")
                    return redirect('users:login')

                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated successfully!")
                return redirect('users:profile')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Your password has been updated successfully!")
                return redirect('users:profile')

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })

# Delete Account
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('users:login')
    return render(request, 'users/profile.html', {'user': request.user})