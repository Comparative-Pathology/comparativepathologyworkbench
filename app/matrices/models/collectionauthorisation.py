#!/usr/bin/python3
###!
# \file         collectionauthorisation.py
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
# The Collection Authorisation Model.
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
from django.utils.translation import gettext_lazy as _

from random import randint

from matrices.models import Collection
from matrices.models import CollectionAuthority


"""
    COLLECTION AUTHORISATION (for Collections)
"""
class CollectionAuthorisation(models.Model):
    collection = models.ForeignKey(Collection, related_name='collectionauthorisations', on_delete=models.CASCADE)
    permitted = models.ForeignKey(User, related_name='collectionauthorisations', on_delete=models.DO_NOTHING)
    collection_authority = models.ForeignKey(CollectionAuthority, related_name='collectionauthorisations', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, collection, permitted, collection_authority):
        return cls(collection=collection, permitted=permitted, collection_authority=collection_authority)

    def __str__(self):
        return f"{self.id}, {self.collection.id}, {self.permitted.id}, {self.collection_authority.id}"

    def __repr__(self):
        return f"{self.id}, {self.collection.id}, {self.permitted.id}, {self.collection_authority.id}"


    def set_collection(self, a_collection):
        self.collection = a_collection

    def is_permitted_by(self, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False

    def set_permitted(self, a_user):
        self.permitted = a_user

    def is_collection_authority(self, a_collection_authority):
        if self.collection_authority == a_collection_authority:
            return True
        else:
            return False

    def set_collection_authority(self, a_collection_authority):
        self.collection_authority = a_collection_authority

    def has_collection_authority(self, a_collection, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False
