#!/usr/bin/python3
###!
# \file         document.py
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
# The Document Model - for items that are uploaded to the CPW ;-)
###
from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib, requests

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from random import randint

from requests.exceptions import HTTPError

from matrices.models import Server


"""
    DOCUMENT
"""
class Document(models.Model):
    comment = models.TextField(max_length=4095, default='')
    source_url = models.CharField(max_length=255, blank=False, default='')
    location = models.FileField(upload_to='', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'pdf', 'svg'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='uploads', on_delete=models.DO_NOTHING)

    def set_comment(self, a_comment):
        self.comment = a_comment

    def set_source_url(self, a_source_url):
        self.source_url = a_source_url

    def set_location(self, a_location):
        self.location = a_location

    def set_uploaded_at(self, an_uploaded_at):
        self.uploaded_at = an_uploaded_at

    def set_owner(self, a_user):
        self.owner = a_user


    @classmethod
    def create(cls, comment, source_url, location, uploaded_at, owner):
        return cls(comment=comment, source_url=source_url, location=location, uploaded_at=uploaded_at)

    def __str__(self):
        return f"{self.id}, {self.comment}, {self.source_url}, {self.location}, {self.uploaded_at}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.comment}, {self.source_url}, {self.location}, {self.uploaded_at}, {self.owner.id}"


    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def is_duplicate(self, a_comment, a_source_url, a_location, an_uploaded_at, a_owner):
        if self.comment == a_comment and self.source_url == a_source_url and self.location == a_location and self.uploaded_at == an_uploaded_at and self.owner == a_owner:
            return True
        else:
            return False
