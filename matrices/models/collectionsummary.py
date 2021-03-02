from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib, requests

from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.signals import post_save
from django.apps import apps
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from random import randint
from decouple import config


"""
    MATRIX SUMMARY (a VIEW for ALL Benches)
"""
class CollectionSummary(models.Model):
    collection_id = models.IntegerField(default=0, blank=False)
    collection_title = models.CharField(max_length=255, default='')
    collection_description = models.TextField(max_length=4095, default='')
    collection_owner = models.CharField(max_length=50, default='')
    collection_active = models.BooleanField(default=True)
    collection_image_count = models.IntegerField(default=0, blank=False)
    collection_authorisation_id = models.IntegerField(default=0, blank=False)
    collection_authorisation_permitted = models.CharField(max_length=50, default='')
    collection_authorisation_authority = models.CharField(max_length=12, default='')


    class Meta:
        managed = False
        db_table = 'matrices_collection_summary'

    def __str__(self):
        return f"{self.collection_id}, {self.collection_title}, {self.collection_description}, {self.collection_owner}, {self.collection_description}, {self.collection_active}, {self.collection_image_count}, {self.collection_authorisation_permitted}, {self.collection_authorisation_authority}"

    def __repr__(self):
        return f"{self.collection_id}, {self.collection_title}, {self.collection_description}, {self.collection_owner}, {self.collection_description}, {self.collection_active}, {self.collection_image_count}, {self.collection_authorisation_permitted}, {self.collection_authorisation_authority}"


    def is_active(self):
        if self.collection_active == True:
            return True
        else:
            return False

    def is_inactive(self):
        if self.collection_active == False:
            return True
        else:
            return False
