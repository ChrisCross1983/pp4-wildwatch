from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserUpdateForm, ProfileUpdateForm


# Signup View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Username: {username}, Password: {password}")
            user = authenticate(request, username=username, password=password)
            print(f"Authenticated user: {user}")

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('users:login')

# Home View
def home(request):
    if request.user.is_authenticated:
        context = {'user': request.user}
    else:
        context = {}
    return render(request, 'users/home.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

# Edit Profile View
@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'save_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated successfully!")
                return redirect('users:profile')
        
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Your password has been updated successfully!")
                return redirect('users:profile')

    else:
        user_form = CustomUserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })