#!/usr/bin/python3
###!
# \file         artefact.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# The Artefact Model - for items that are uploaded to the CPW when Images are linked
###
from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib, requests

from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _



"""
    ARTEFACT
"""
class Artefact(models.Model):
    comment = models.TextField(max_length=4095, default='')
    location = models.FileField(upload_to='', validators=[FileExtensionValidator(['zip'])], max_length=500, blank=True)
    url = models.CharField(max_length=255, blank=False, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='artefacts', on_delete=models.DO_NOTHING)

    def set_comment(self, a_comment):
        self.comment = a_comment

    def set_location(self, a_location):
        self.location = a_location

    def set_url(self, a_url):
        self.url = a_url

    def set_uploaded_at(self, an_uploaded_at):
        self.uploaded_at = an_uploaded_at

    def set_owner(self, a_user):
        self.owner = a_user


    @classmethod
    def create(cls, comment, location, url, uploaded_at, owner):
        return cls(comment=comment, location=location, url=url, uploaded_at=uploaded_at)

    def __str__(self):
        return f"{self.id}, {self.comment}, {self.location}, {self.url}, {self.uploaded_at}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.comment}, {self.location}, {self.url}, {self.uploaded_at}, {self.owner.id}"


    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def is_duplicate(self, a_comment, a_location, an_uploaded_at, a_owner):
        if self.comment == a_comment and self.location == a_location and self.url == url and self.uploaded_at == an_uploaded_at and self.owner == a_owner:
            return True
        else:
            return False

    def has_location(self):

        if self.location == "":
            return False
        else:
            return True

    def get_location_minus_path(self):

        path_array = self.location.name.split("/")

        return path_array[6]
