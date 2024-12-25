from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
from datetime import timedelta
import uuid
import logging
from users.models import Profile
from django.db import IntegrityError

logger = logging.getLogger(__name__)

def generate_token():
    """Generate a unique token using UUID."""
    return str(uuid.uuid4())

def send_verification_email(user):
    try:
        # Ensure the profile exists and generate a token
        profile, created = Profile.objects.get_or_create(user=user)
        token = generate_token()
        profile.email_token = token
        profile.email_token_expiry = now() + timedelta(days=3)
        profile.save()

        # Use static domain for verification link
        domain = getattr(settings, "DEFAULT_DOMAIN", "127.0.0.1:8000")
        verification_link = f"http://{domain}/users/confirm-email/{token}/"

        # Send verification email
        send_mail(
            subject="Verify your email address",
            message=(
                f"Hi {user.username},\n\n"
                f"Please click the following link to verify your email address:\n"
                f"{verification_link}\n\n"
                f"If you didn’t request this email, you can safely ignore it.\n\n"
                f"Best regards,\nThe Wild Watch Team"),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {e}")
        raise
