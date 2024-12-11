#!/usr/bin/python3
#
# ##
# \file         authority.py
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
# The Bench Authority Model.
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

AUTHORITY_NONE = 'NONE'
AUTHORITY_EDITOR = 'EDITOR'
AUTHORITY_VIEWER = 'VIEWER'
AUTHORITY_OWNER = 'OWNER'
AUTHORITY_ADMIN = 'ADMIN'


#
#    The Authority Manager Class
#
class AuthorityManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Authority.DoesNotExist):

            return None


#
#   AUTHORITY (for Bench Authorisations)
#
class Authority(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='authorities', on_delete=models.DO_NOTHING)

    objects = AuthorityManager()

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
        self.name = AUTHORITY_NONE

    def set_as_editor(self):
        self.name = AUTHORITY_EDITOR

    def set_as_viewer(self):
        self.name = AUTHORITY_VIEWER

    def set_as_owner(self):
        self.name = AUTHORITY_OWNER

    def set_as_admin(self):
        self.name = AUTHORITY_ADMIN

    def is_none(self):
        if self.name == AUTHORITY_NONE:
            return True
        else:
            return False

    def is_not_none(self):
        if self.name == AUTHORITY_NONE:
            return False
        else:
            return True

    def is_editor(self):
        if self.name == AUTHORITY_EDITOR:
            return True
        else:
            return False

    def is_not_editor(self):
        if self.name == AUTHORITY_EDITOR:
            return False
        else:
            return True

    def is_viewer(self):
        if self.name == AUTHORITY_VIEWER:
            return True
        else:
            return False

    def is_not_viewer(self):
        if self.name == AUTHORITY_VIEWER:
            return False
        else:
            return True

    def is_owner(self):
        if self.name == AUTHORITY_OWNER:
            return True
        else:
            return False

    def is_not_owner(self):
        if self.name == AUTHORITY_OWNER:
            return False
        else:
            return True

    def is_admin(self):
        if self.name == AUTHORITY_ADMIN:
            return True
        else:
            return False

    def is_not_admin(self):
        if self.name == AUTHORITY_ADMIN:
            return False
        else:
            return True
