from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib, requests

from django.db import models
from django.db.models import Q 
from django.db.models import Count
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from random import randint
from decouple import config


"""
    PROFILE
"""
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    @classmethod
    def create(cls, user, bio, location, birth_date, email_confirmed):
        return cls(user=user, bio=bio, location=location, birth_date=birth_date, email_confirmed=email_confirmed)
    
    def __str__(self):
        return f"{self.id}, {self.bio}, {self.location}, {self.birth_date}, {self.email_confirmed}"
        
    def __repr__(self):
        return f"{self.id}, {self.user.id}, {self.bio}, {self.location}, {self.birth_date}, {self.email_confirmed}"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

