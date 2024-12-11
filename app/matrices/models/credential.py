#!/usr/bin/python3
#
# ##
# \file         credential.py
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
# The (Wordpress Blog) Credential Model.
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


#
#    The Credential Manager Class
#
class CredentialManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Credential.DoesNotExist):

            return None


#
#   CREDENTIAL (for a User)
#
class Credential(models.Model):
    username = models.CharField(max_length=50, blank=False, unique=True)
    wordpress = models.IntegerField(default=0, blank=False)
    apppwd = models.CharField(max_length=50, blank=True, default='')
    owner = models.ForeignKey(User, related_name='credentials', on_delete=models.DO_NOTHING)

    objects = CredentialManager()

    @classmethod
    def create(cls, username, wordpress, apppwd, owner):
        return cls(username=username, wordpress=wordpress, apppwd=apppwd, owner=owner)

    def __str__(self):
        return f"{self.id}, {self.username}, {self.wordpress}, {self.apppwd}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.wordpress}, {self.apppwd}, {self.owner.id}"

    def has_no_apppwd(self):
        if self.apppwd == '':
            return True
        else:
            return False

    def has_apppwd(self):
        if self.apppwd == '':
            return False
        else:
            return True

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def set_owner(self, a_user):
        self.owner = a_user
