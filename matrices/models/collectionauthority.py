#!/usr/bin/python3
###!
# \file         collectionauthority.py
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
# The Collection Authority Model.
###
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
    COLLECTION AUTHORITY (for Collection Authorisations)
"""
class CollectionAuthority(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='collectionauthorities', on_delete=models.DO_NOTHING)

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

    def set_as_viewer(self):
        self.name = 'VIEWER'

    def is_none(self):
        if self.name == 'NONE':
            return True
        else:
            return False

    def is_viewer(self):
        if self.name == 'VIEWER':
            return True
        else:
            return False
