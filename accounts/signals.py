from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


post_save.connect(receiver=create_profile, sender=User)


# این گونه هم میتوان اینکار را هندل کرد
# @receiver(signal=post_save, sender=User)
# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         Profile.objects.create(user=kwargs['instance'])
