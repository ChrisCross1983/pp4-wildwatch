from django.urls import path, include
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import signup, profile, edit_profile, delete_account, login_view, logout_view, home, signup_thanks, confirm_email, email_confirm_resend, CustomPasswordResetView

def set_dynamic_site():
    try:
        if settings.DEBUG:
            Site.objects.update_or_create(id=1, defaults={
                'domain': '127.0.0.1:8000',
                'name': 'WildWatch Local'
            })
        else:
            Site.objects.update_or_create(id=1, defaults={
                'domain': 'wild-watch-4ac96b54e024.herokuapp.com',
                'name': 'WildWatch Heroku'
            })
    except (OperationalError, ProgrammingError):
        pass

set_dynamic_site()

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
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url='/users/password-reset-complete/'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
