from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile

# Custom Form for User Signup
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(max_length=254, required=True, label="Email")
    profile_picture = forms.ImageField(required=False, label="Upload Profile Picture")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()

            profile_picture = self.cleaned_data.get('profile_picture')
            profile, created = Profile.objects.get_or_create(user=user)
            if profile_picture:
                profile.profile_picture = profile_picture
            else:
                profile.profile_picture = 'https://res.cloudinary.com/duazmtlpi/image/upload/v1735380047/placeholder_werhfs.jpg'
            profile.save()
        return user

# Custom Form for Editing User Details
class CustomUserUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, label="Change Profile Picture")
    email = forms.EmailField(max_length=254, required=True, label="Email")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=150, required=True, label="Username")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.strip():
            raise forms.ValidationError("First Name cannot be empty.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.strip():
            raise forms.ValidationError("Last Name cannot be empty.")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.strip():
            raise forms.ValidationError("Username cannot be empty.")
        return username

# Form for Editing Profile-Specific Details
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('profile_picture'):
            cleaned_data['profile_picture'] = 'profile_pictures/placeholder.jpg'
        return cleaned_data
