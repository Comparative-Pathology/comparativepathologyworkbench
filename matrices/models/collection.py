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


from matrices.models import Image


"""
    COLLECTION
"""
class Collection(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    images = models.ManyToManyField(Image, related_name='collections')
    
    @classmethod
    def create(cls, title, description, active, owner):
        return cls(title=title, description=description, active=active, owner=owner)
    
    @classmethod
    def assign_image(cls, current_image, new_collection):
        new_collection.images.add(current_image)
    
    @classmethod
    def unassign_image(cls, current_image, cancel_collection):
        cancel_collection.images.remove(current_image)
    
    def __str__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.active}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.active}, {self.owner.id}"

    def set_matrix(self, a_matrix):
        self.matrix = a_matrix

    def set_title(self, a_title):
        self.title = a_title

    def set_description(self, a_description):
        self.description = a_description

    def set_owner(self, a_user):
        self.owner = a_user

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def set_active(self):
        self.active = True
        
    def set_inactive(self):
        self.active = False
        
    def is_active(self):
        if self.active == True:
            return True
        else:
            return False

    def is_inactive(self):
        if self.active == False:
            return True
        else:
            return False
            
