#!/usr/bin/python3
#
# ##
# \file         imagelink.py
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
# The Image Link Model
# ##
#
from __future__ import unicode_literals

from django.db import models

from matrices.models import Image
from matrices.models import Artefact


#
#    The ImageLinkage Manager Class
#
class ImageLinkManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, ImageLink.DoesNotExist):

            return None


#
#   IMAGE
#
class ImageLink(models.Model):
    parent_image = models.ForeignKey(Image, related_name='parent', on_delete=models.DO_NOTHING)
    child_image = models.ForeignKey(Image, related_name='child', on_delete=models.DO_NOTHING)
    artefact = models.ForeignKey(Artefact, related_name='file', on_delete=models.DO_NOTHING)

    objects = ImageLinkManager()

    def set_parent_image(self, a_parent_image):
        self.parent_image = a_parent_image

    def set_child_image(self, a_child_image):
        self.child_image = a_child_image

    def set_artefact(self, a_artefact):
        self.artefact = a_artefact

    @classmethod
    def create(cls, parent_image, child_image, artefact):
        return cls(parent_image=parent_image, child_image=child_image, artefact=artefact)

    def __str__(self):
        return f"{self.id}, {self.parent_image.id}, {self.child_image.id}, {self.artefact.id}"

    def __repr__(self):
        return f"{self.id}, {self.parent_image.id}, {self.child_image.id}, {self.artefact.id}"

    def is_duplicate(self, a_parent_image, a_child_image, a_artefact):
        if self.parent_image == a_parent_image and self.child_image == a_child_image and self.artefact == a_artefact:
            return True
        else:
            return False

    def get_owner(self):
        return self.artefact.owner

    def is_owned_by(self, a_user):
        if self.get_owner() == a_user:
            return True
        else:
            return False
