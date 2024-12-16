from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

# Custom Form for User Signup
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    profile_picture = forms.ImageField(required=False, label="Upload Profile Picture")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Profile.objects.create(user=user, profile_picture=self.cleaned_data.get('profile_picture'))
        return user

# Custom Form for Editing User Details
class CustomUserUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, label="Change Profile Picture")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

# Form for Editing Profile-Specific Details
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
