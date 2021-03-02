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
class MatrixSummary(models.Model):
    matrix_id = models.IntegerField(default=0, blank=False)
    matrix_title = models.CharField(max_length=255, default='')
    matrix_description = models.TextField(max_length=4095, default='')
    matrix_blogpost = models.CharField(max_length=50, blank=True, default='')
    matrix_created = models.DateTimeField()
    matrix_modified = models.DateTimeField()
    matrix_height = models.IntegerField(default=0, blank=False)
    matrix_width = models.IntegerField(default=0, blank=False)
    matrix_owner = models.CharField(max_length=50, default='')
    matrix_authorisation_id = models.IntegerField(default=0, blank=False)
    matrix_authorisation_permitted = models.CharField(max_length=50, default='')
    matrix_authorisation_authority = models.CharField(max_length=12, default='')

    class Meta:
        managed = False
        db_table = 'matrices_bench_summary'
        
    def __str__(self):
        return f"{self.matrix_id}, {self.matrix_title}, {self.matrix_description}, {self.matrix_blogpost}, {self.matrix_created}, {self.matrix_modified}, {self.matrix_height}, {self.matrix_width}, {self.matrix_owner}, {self.matrix_authorisation_id}, {self.matrix_authorisation_permitted}, {self.matrix_authorisation_authority}"
        
    def __repr__(self):
        return f"{self.matrix_id}, {self.matrix_title}, {self.matrix_description}, {self.matrix_blogpost}, {self.matrix_created}, {self.matrix_modified}, {self.matrix_height}, {self.matrix_width}, {self.matrix_owner}, {self.matrix_authorisation_id}, {self.matrix_authorisation_permitted}, {self.matrix_authorisation_authority}"

        
