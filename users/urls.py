from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup, profile, edit_profile, delete_account, login_view, logout_view, home, signup_thanks, confirm_email, email_confirm_resend

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('signup/', signup, name='signup'),
    path('signup/thanks/', signup_thanks, name='signup_thanks'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),

    # Profile Management
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-account/', delete_account, name='delete_account'),

    # Confirm Email Pages
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),
    path('resend-email/', email_confirm_resend, name='email_confirm_resend'),

    # Password Reset URLs
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html', success_url='/users/password-reset/done/'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url='/users/password-reset-complete/'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
