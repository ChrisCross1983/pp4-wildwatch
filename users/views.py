from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomPasswordResetForm, CustomUserUpdateForm, ProfileUpdateForm
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .utils import send_verification_email
from django.utils.timezone import now
from django.db import connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Signup View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            profile = Profile.objects.create(user=user)
            profile.profile_picture = form.cleaned_data.get('profile_picture') or 'profile_pictures/placeholder.jpg'
            profile.save()

            send_verification_email(user)
            messages.success(
                request,
                "Account created successfully. Please check your email to activate your account.")

            return HttpResponseRedirect(reverse('users:signup_thanks'))
        else:
            messages.error(request, "There was an error in your registration.")
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

        # User is already verified
        if profile.user.is_active:
            messages.info(request, "Your email is already verified. You can log in.")
            return redirect("users:login")

        # Token is expired
        if profile.email_token_expiry and profile.email_token_expiry < now():
            messages.warning(request, "This token has expired. Please request a new confirmation email.")
            return redirect("users:email_confirm_resend")

        # Token is valig - Confirm E-Mail
        profile.user.is_active = True
        profile.email_token = None
        profile.email_token_expiry = None
        profile.user.save()

        if not profile.profile_picture:
            profile.profile_picture = 'profile_pictures/placeholder.jpg'
        profile.save()

        messages.success(request, "Your email has been confirmed! You can now log in.")
        return redirect("users:login")

    except Profile.DoesNotExist:
        # Token belongs to no profile (perhaps already verified)
        # Checks, if the user is existing and active
        user_exists = Profile.objects.filter(user__is_active=True).exists()
        if user_exists:
            messages.info(request, "Your email is already verified. You can log in.")
            return redirect("users:login")

        # Token is completly invalid or manipulated
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
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            
            if not user.is_active:
                messages.warning(request, "Your account is not verified. Please check your email or request a new verification link.")
                return redirect("users:email_confirm_resend")

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "Invalid password.")
                return redirect("users:login")

            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home")

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("users:login")

    else:
        form = AuthenticationForm()

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
    logger.info("Edit profile view accessed")
    profile = request.user.profile
    old_email = request.user.email

    if request.method == 'POST':

        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if 'save_profile' in request.POST:
            logger.info("Save Profile Button Clicked")

            user_form_valid = user_form.is_valid()
            profile_form_valid = profile_form.is_valid()

            if user_form_valid and profile_form_valid:

                user = user_form.save(commit=False)

                if old_email != user_form.cleaned_data['email']:
                    user.is_active = False
                    user.save()
                    send_verification_email(user)
                    messages.success(request, "Your email was updated. Please verify your new email.")

                    logout(request)
                    return redirect('users:login')

                user.save()

                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE auth_user
                        SET first_name = %s,
                            last_name = %s,
                            email = %s,
                            username = %s
                        WHERE id = %s
                    """, [
                        user_form.cleaned_data['first_name'],
                        user_form.cleaned_data['last_name'],
                        user_form.cleaned_data['email'],
                        user_form.cleaned_data['username'],
                        request.user.pk
                    ])

                request.user.refresh_from_db()

                saved_user = User.objects.get(pk=request.user.pk)

                if 'profile_picture' in request.FILES:
                    profile_picture = profile_form.cleaned_data.get('profile_picture')

                    if profile_picture:
                        from cloudinary.uploader import upload, destroy
                        try:
                            if profile.profile_picture and isinstance(profile.profile_picture, str):
                                destroy(profile.profile_picture)

                            upload_result = upload(profile_picture.file)
                            profile.profile_picture = upload_result['public_id']
                            profile.save()

                        except Exception as e:
                            messages.error(request, "There was an error uploading the profile picture.")

                messages.success(request, "Your profile has been updated successfully!")

                return redirect('users:profile')
            else:
                messages.error(request, "There was an error updating your profile. Please check the form for errors.")
        else:
            logger.warning("Save Profile button not found in POST request.")
    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
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

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'registration/password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_secure() or not settings.DEBUG:
            context['protocol'] = 'https'
        else:
            context['protocol'] = 'http'
        context['domain'] = settings.DEFAULT_DOMAIN
        return context
