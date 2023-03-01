#!/usr/bin/python3
###!
# \file         collection.py
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
# The (Image) Collection Model.
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

from matrices.models import Image


"""
    COLLECTION
"""
class Collection(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    images = models.ManyToManyField(Image, related_name='collections')

    @classmethod
    def create(cls, title, description, owner):
        return cls(title=title, description=description, owner=owner)

    @classmethod
    def assign_image(cls, current_image, new_collection):
        new_collection.images.add(current_image)

    @classmethod
    def unassign_image(cls, current_image, cancel_collection):
        cancel_collection.images.remove(current_image)

    def __str__(self):
        return f"{self.id:06d}, {self.owner.username}, {self.title}"

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.owner.id}"

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
