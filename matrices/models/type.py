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
    TYPE
"""
class Type(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='types', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, name, owner):
        return cls(name=name, owner=owner)
    
    def __str__(self):
        return f"{self.name}"
        
    def __repr__(self):
        return f"{self.name}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        
