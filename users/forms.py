from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Profile
from cloudinary.api import resource
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload, destroy

User = get_user_model()

# Custom Form for User Signup

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(max_length=254, required=True, label="Email")
    profile_picture = forms.ImageField(
        required=False,
        label="Upload Profile Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

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
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="Email",
        widget=forms.TextInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'autocomplete': 'given-name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'autocomplete': 'family-name', 'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        print("User Object Before Save:", user.__dict__)

        if commit:
            user.save()
            print("User Object After Save:", user.__dict__)
        return user

# Form for Editing Profile-Specific Details
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and hasattr(picture, 'size'):
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("The image should be not bigger than 5 MB.")
        return picture

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile_picture = self.cleaned_data.get('profile_picture')

        if profile_picture:
            try:
                upload_result = upload(profile_picture.file)
                profile.profile_picture = upload_result['public_id']
            except Exception as e:
                print("Error uploading profile picture:", e)
                raise forms.ValidationError("There was an error while uploading your profile picture. Please try again later.")

        if commit:
            profile.save()
        return profile

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise ValidationError(_("No account found with this email address."))

        return email
