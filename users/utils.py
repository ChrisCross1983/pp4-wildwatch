from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.sites.models import Site
import uuid
import logging
from datetime import timedelta
from users.models import Profile

logger = logging.getLogger(__name__)

def generate_token():
    """Generate a unique token using UUID."""
    return str(uuid.uuid4())

def send_verification_email(user, request=None):
    try:
        profile, created = Profile.objects.get_or_create(user=user)
        token = generate_token()
        profile.email_token = token
        profile.email_token_expiry = now() + timedelta(days=3)
        profile.save()

        if request:
            domain = request.get_host()
        else:
            domain = getattr(settings, "DEFAULT_DOMAIN", None)
            if not domain and "django.contrib.sites" in settings.INSTALLED_APPS:
                domain = Site.objects.get_current().domain
            if not domain:
                domain = "127.0.0.1:8000"

        protocol = "https" if not settings.DEBUG else "http"
        verification_link = f"{protocol}://{domain}/users/confirm-email/{token}/"

        # Send verification email
        send_mail(
            subject="Verify your email address",
            message=(
                f"Hi {user.username},\n\n"
                f"Please click the following link to verify your email address:\n"
                f"{verification_link}\n\n"
                f"If you didn’t request this email, you can safely ignore it.\n\n"
                f"Best regards,\nThe Wild Watch Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {e}")
        raise
