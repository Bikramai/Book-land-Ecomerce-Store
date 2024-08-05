from django.db.models.signals import post_save
from django.dispatch import receiver

from src.accounts.models import User, Address


@receiver(post_save, sender=User)
def create_Address(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)
