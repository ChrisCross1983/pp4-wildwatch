from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    profile_picture = forms.ImageField(required=False)

class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'password1', 'password2']

class CustomUserUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, label="Change Profile Picture")
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
