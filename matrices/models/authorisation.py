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


from matrices.models import Matrix
from matrices.models import Authority


"""
    AUTHORISATION (for a Bench)
"""
class Authorisation(models.Model):
    matrix = models.ForeignKey(Matrix, related_name='authorisations', on_delete=models.CASCADE, verbose_name=_('Bench'))
    permitted = models.ForeignKey(User, related_name='authorisations', on_delete=models.DO_NOTHING)
    authority = models.ForeignKey(Authority, related_name='authorisations', on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name = _('Authorisation')
        verbose_name_plural = _('Authorisations')
        
    @classmethod
    def create(cls, matrix, permitted, authority):
        return cls(matrix=matrix, permitted=permitted, authority=authority)
    
    def __str__(self):
        return f"{self.id}, {self.matrix.id}, {self.permitted.id}, {self.authority.id}"

    def __repr__(self):
        return f"{self.id}, {self.matrix.id}, {self.permitted.id}, {self.authority.id}"


    def set_matrix(self, a_matrix):
        self.matrix = a_matrix

    def is_permitted_by(self, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False
            
    def set_permitted(self, a_user):
        self.permitted = a_user
        
    def is_authority(self, a_authority):
        if self.authority == a_authority:
            return True
        else:
            return False
            
    def set_authority(self, a_authority):
        self.authority = a_authority
        
    def has_authority(self, a_matrix, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False

