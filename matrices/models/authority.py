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
    AUTHORITY (for Bench Authorisations)
"""
class Authority(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='authorities', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, name, owner):
        return cls(name=name, owner=owner)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user

    def set_as_none(self):
        self.name = 'NONE'

    def set_as_editor(self):
        self.name = 'EDITOR'

    def set_as_viewer(self):
        self.name = 'VIEWER'

    def set_as_owner(self):
        self.name = 'OWNER'

    def set_as_admin(self):
        self.name = 'ADMIN'

    def is_none(self):
        if self.name == 'NONE':
            return True
        else:
            return False
            
    def is_not_none(self):
        if self.name == 'NONE':
            return False
        else:
            return True
            
    def is_editor(self):
        if self.name == 'EDITOR':
            return True
        else:
            return False
            
    def is_not_editor(self):
        if self.name == 'EDITOR':
            return False
        else:
            return True
            
    def is_viewer(self):
        if self.name == 'VIEWER':
            return True
        else:
            return False

    def is_not_viewer(self):
        if self.name == 'VIEWER':
            return False
        else:
            return True

    def is_owner(self):
        if self.name == 'OWNER':
            return True
        else:
            return False

    def is_not_owner(self):
        if self.name == 'OWNER':
            return False
        else:
            return True
        
    def is_admin(self):
        if self.name == 'ADMIN':
            return True
        else:
            return False

    def is_not_admin(self):
        if self.name == 'ADMIN':
            return False
        else:
            return True

