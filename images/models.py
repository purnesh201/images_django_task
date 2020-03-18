# -*- coding: utf-8 -*-
# python
from __future__ import unicode_literals
# libs
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


class TimeStampedModel(models.Model):
    '''
    Tracking record created, updated and deleted 
    date, time.
    '''
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class User(AbstractUser):

    Allowed_IP = models.GenericIPAddressField(default='127.0.0.1')
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return f"User {self.pk}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class images(models.Model):
    name = models.CharField('imageName', max_length=255)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='imageData/default_image.jpg', upload_to='imageData', null=True, blank=True)

    def __str__(self):
        return f"idImage {self.pk}"

