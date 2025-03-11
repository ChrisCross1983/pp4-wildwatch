from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from cloudinary.models import CloudinaryField
import uuid
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    email_token_expiry = models.DateTimeField(null=True, blank=True)
    profile_picture = CloudinaryField(
        'image',
        default='profile_pictures/placeholder',
        blank=True,
        null=True
    )
    
    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'https://res.cloudinary.com/duazmtlpi/image/upload/v1735562779/profile_pictures/placeholder.jpg'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"
