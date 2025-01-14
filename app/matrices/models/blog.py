#!/usr/bin/python3
#
# ##
# \file         blog.py
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
# The Blog (Wordpress API command) Model.
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from matrices.models import Protocol


#
#    The Blog Manager Class
#
class BlogManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Blog.DoesNotExist):

            return None


#
#   BLOG (Command)
#
class Blog(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    protocol = models.ForeignKey(Protocol, related_name='blogs', default=0, on_delete=models.CASCADE)
    application = models.CharField(max_length=25, blank=True, default='')
    preamble = models.CharField(max_length=50, blank=True, default='')
    postamble = models.CharField(max_length=50, blank=True, default='')
    owner = models.ForeignKey(User, related_name='blogs', on_delete=models.DO_NOTHING)

    objects = BlogManager()

    @classmethod
    def create(cls, name, protocol, application, preamble, postamble, owner):
        return cls(name=name, protocol=protocol, application=application, preamble=preamble, postamble=postamble, 
                   owner=owner)

    def __str__(self):
        return (
            f"{self.id}, {self.name}, {self.protocol.id}, {self.application}, {self.preamble}, "
            f"{self.postamble}, {self.owner.id}"
        )

    def __repr__(self):
        return (
            f"{self.id}, {self.name}, {self.protocol.id}, {self.application}, {self.preamble}, "
            f"{self.postamble}, {self.owner.id}"
        )

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def set_owner(self, a_user):
        self.owner = a_user
