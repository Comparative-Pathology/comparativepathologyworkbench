#!/usr/bin/python3
#
# ##
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
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from matrices.models import Image


#
#    The Collection Manager Class
#
class CollectionManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Collection.DoesNotExist):

            return None


#
#   The Collection Model
#
class Collection(models.Model):

    title = models.CharField(max_length=255,
                             default='')
    description = models.TextField(max_length=4095,
                                   default='')
    owner = models.ForeignKey(User,
                              on_delete=models.DO_NOTHING)
    images = models.ManyToManyField(Image,
                                    related_name='collections')
    locked = models.BooleanField(default=False)

    objects = CollectionManager()

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
        return f"{self.id:06d}, {self.owner.username}, {self.title}, {self.locked}"

    def __repr__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.owner.id}, {self.locked}"

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

    #
    #   If this Collection is Locked, then True, else False
    #
    def is_locked(self):

        if self.locked is True:
            return True
        else:
            return False

    #
    #   If this Collection is NOT Locked, then True, else False
    #
    def is_not_locked(self):

        if self.locked is False:
            return True
        else:
            return False

    #
    #   If this Collection is Unlocked, then True, else False
    #
    def is_unlocked(self):

        if self.locked is False:
            return True
        else:
            return False

    #
    #   If this Collection is NOT Locked, then True, else False
    #
    def is_not_unlocked(self):

        if self.locked is True:
            return True
        else:
            return False

    #
    #   Sets the Locked field of the Collection to True
    #
    def set_locked(self):

        self.locked = True

    #
    #   Sets the Locked field of the Collection to False
    #
    def set_unlocked(self):

        self.locked = False

    def get_tags(self):

        collection_tag_list = list()

        collection_image_list = self.get_images()

        for image in collection_image_list:

            for tag in image.tags.all():

                if tag not in collection_tag_list:

                    collection_tag_list.append(tag)

        return collection_tag_list

    def get_images(self):
        return self.images.filter(Q(hidden=False))

    def get_images_count(self):
        return self.images.filter(Q(hidden=False)).count()

    def get_hidden_images(self):
        return self.images.filter(Q(hidden=True))

    def get_hidden_images_count(self):
        return self.images.filter(Q(hidden=True)).count()

    def get_images_for_tag(self, a_tag):
        return self.images.filter(Q(hidden=False)).filter(tags__name__in=[a_tag.name])

    def get_all_images(self):
        return self.images.all()

    #
    #   Returns the Formatted ID for the Collection
    #
    def get_formatted_id(self):

        return format(int(self.id), '06d')
