import random
import string
import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from onlineshop.utils.db.validators import phone_nuber_validator


# Create your models here.

class MyUser(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='users',on_delete=models.CASCADE)

    @receiver(post_save, sender=MyUser)
    def _post_save_receiver(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


class OTPrequest(models.Model):
    class OTPChannel(models.TextChoices):
        WEB = _('web')
        ANDROID = _('android')
        IOS = _('ios')

    request_id = models.UUIDField(primary_key=True,editable=True,default=uuid.uuid4)
    channel = models.CharField(_('Channel'),max_length=7,choices=OTPChannel.choices,default=OTPChannel.WEB)
    phone = models.CharField(_('Phone Number'),max_length=12)
    password = models.CharField(max_length=4,null=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(timezone.now()+timedelta(seconds=120))
    receive_id = models.CharField(max_length=255, null=True)

    def generate_password(self):
        self.password = self._random_password()
        self.valid_until = timezone.now()+timedelta(seconds=120)

    def _random_password(self):
        rand = random.SystemRandom()
        digit = rand.choices(string.digits,k=4)
        return ''.join(digit)



    class Meta:
        verbose_name = _('One Time Password')
        verbose_name_plural = ('One Time Passwords ')
