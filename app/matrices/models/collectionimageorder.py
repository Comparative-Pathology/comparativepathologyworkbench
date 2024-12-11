#!/usr/bin/python3
#
# ##
# \file         collectionimageorder.py
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
# The Collection Image Order Model.
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from matrices.models import Collection
from matrices.models import Image


#
#    The CollectionImageOrder Manager Class
#
class CollectionImageOrderManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, CollectionImageOrder.DoesNotExist):

            return None


#
#   The Collection Image Order Model (for Collections, Images and Users)
#
class CollectionImageOrder(models.Model):

    collection = models.ForeignKey(Collection,
                                   related_name='collectionimageorders',
                                   on_delete=models.CASCADE)
    image = models.ForeignKey(Image,
                              related_name='collectionimageorders',
                              on_delete=models.CASCADE)
    permitted = models.ForeignKey(User,
                                  related_name='collectionimageorders',
                                  on_delete=models.DO_NOTHING)
    ordering = models.IntegerField(default=0)

    objects = CollectionImageOrderManager()

    @classmethod
    def create(cls, collection, image, permitted, ordering):
        return cls(collection=collection, image=image, permitted=permitted, ordering=ordering)

    def __str__(self):
        return f"{self.id}, {self.collection.id}, {self.image.id}, {self.permitted.id}, {self.ordering}"

    def __repr__(self):
        return f"{self.id}, {self.collection.id}, {self.image.id}, {self.permitted.id}, {self.ordering}"

    def set_collection(self, a_collection):
        self.collection = a_collection

    def set_image(self, a_image):
        self.image = a_image

    def set_permitted(self, a_user):
        self.permitted = a_user

    def set_ordering(self, a_ordering):
        self.ordering = a_ordering

    def is_collection(self, a_collection):
        if self.collection == a_collection:
            return True
        else:
            return False

    def is_image(self, a_image):
        if self.image == a_image:
            return True
        else:
            return False

    def is_permitted_by(self, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False

    def decrement_ordering(self):
        self.ordering = self.ordering - 1

    def increment_ordering(self):
        self.ordering = self.ordering + 1
