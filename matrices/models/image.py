#!/usr/bin/python3
###!
# \file         image.py
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
# The Image Model - should really be "Thing" ;-)
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
from decouple import config

from requests.exceptions import HTTPError

from matrices.models import Server



"""
    IMAGE
"""
class Image(models.Model):
    identifier = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=False, default='')
    server = models.ForeignKey(Server, related_name='images', default=0, on_delete=models.CASCADE)
    viewer_url = models.CharField(max_length=255, blank=False, default='')
    birdseye_url = models.CharField(max_length=255, blank=False, default='')
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.DO_NOTHING)
    roi = models.IntegerField(default=0)
    comment = models.TextField(max_length=4095, default='')

    def set_identifier(self, an_identifier):
        self.identifier = an_identifier

    def set_name(self, a_name):
        self.name = a_name

    def set_server(self, a_server):
        self.server = a_server

    def set_viewer_url(self, a_viewer_url):
        self.viewer_url = a_viewer_url

    def set_birdseye_url(self, a_birdseye_url):
        self.birdseye_url = a_birdseye_url

    def set_owner(self, an_owner):
        self.owner = an_owner

    def set_roi(self, a_roi):
        self.roi = a_roi

    def set_comment(self, a_comment):
        self.comment = a_comment

    @classmethod
    def create(cls, identifier, name, server, viewer_url, birdseye_url, roi, owner, comment):
        return cls(identifier=identifier, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url, roi=roi, owner=owner, comment=comment)

    def __str__(self):
        return f"{self.id}, {self.identifier}, {self.name}, {self.server.id}, {self.viewer_url}, {self.birdseye_url}, {self.owner.id}, {self.roi}, {self.comment}"

    def __repr__(self):
        return f"{self.id}, {self.identifier}, {self.name}, {self.server.id}, {self.viewer_url}, {self.birdseye_url}, {self.owner.id}, {self.roi}, {self.comment}"


    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def set_owner(self, a_user):
        self.owner = a_user

    def is_omero_image(self):
        if "iviewer" in self.viewer_url:
            return True
        else:
            return False

    def is_non_omero_image(self):
        if "iviewer" in self.viewer_url:
            return False
        else:
            return True

    def is_duplicate(self, a_identifier, a_name, a_server, a_viewer_url, a_birdseye_url, a_roi, a_owner):
        if self.identifier == a_identifier and self.name == a_name and self.server == a_server and self.viewer_url == a_viewer_url and self.birdseye_url == a_birdseye_url and self.roi == a_roi and self.owner == a_owner:
            return True
        else:
            return False

    def image_id(self):
        return self.identifier
