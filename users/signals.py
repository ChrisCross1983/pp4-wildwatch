from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user: {instance.username}")
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
            logger.info(f"Profile updated for user: {instance.username}")
        else:
            logger.warning(f"No profile found for user: {instance.username}")