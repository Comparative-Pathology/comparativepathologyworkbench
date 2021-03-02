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


from matrices.models import Protocol


"""
    BLOG (Command)
"""
class Blog(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    protocol = models.ForeignKey(Protocol, related_name='blogs', default=0, on_delete=models.CASCADE)
    url_blog = models.CharField(max_length=50, blank=False, default='')
    application = models.CharField(max_length=25, blank=True, default='')
    preamble = models.CharField(max_length=50, blank=True, default='')
    postamble = models.CharField(max_length=50, blank=True, default='')
    owner = models.ForeignKey(User, related_name='blogs', on_delete=models.DO_NOTHING)
    
    @classmethod
    def create(cls, name, protocol, url_blog, application, preamble, postamble, owner):
        return cls(name=name, protocol=protocol, url_blog=url_blog, application=application, preamble=preamble, postamble=postamble, owner=owner)
    
    def __str__(self):
        return f"{self.id}, {self.name}, {self.protocol.id}, {self.url_blog}, {self.application}, {self.preamble}, {self.postamble}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.protocol.id}, {self.url_blog}, {self.application}, {self.preamble}, {self.postamble}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        