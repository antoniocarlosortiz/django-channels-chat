from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.rooms.models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(owner=instance)
        profile.save()
