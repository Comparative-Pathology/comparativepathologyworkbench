#!/usr/bin/python3
#
# ##
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
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from matrices.models import Server

from matrices.routines.exists_parent_image_links_for_image import exists_parent_image_links_for_image
from matrices.routines.get_parent_image_links_for_image import get_parent_image_links_for_image
from matrices.routines.exists_child_image_links_for_image import exists_child_image_links_for_image
from matrices.routines.get_child_image_links_for_image import get_child_image_links_for_image
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment


#
#    The Image Manager Class
#
class ImageManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Image.DoesNotExist):

            return None


#
#   The Image Model
#
class Image(models.Model):

    identifier = models.IntegerField(default=0)
    name = models.CharField(max_length=255,
                            blank=False,
                            default='')
    server = models.ForeignKey(Server,
                               related_name='images',
                               default=0,
                               on_delete=models.CASCADE)
    viewer_url = models.CharField(max_length=255,
                                  blank=False,
                                  default='')
    birdseye_url = models.CharField(max_length=255,
                                    blank=False,
                                    default='')
    owner = models.ForeignKey(User, related_name='owner',
                              on_delete=models.DO_NOTHING)
    roi = models.IntegerField(default=0)
    comment = models.TextField(max_length=4095,
                               default='')
    hidden = models.BooleanField(default=False)

    tags = TaggableManager()

    objects = ImageManager()

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

    def set_hidden(self, a_hidden):
        self.hidden = a_hidden

    @classmethod
    def create(cls, identifier, name, server, viewer_url, birdseye_url, roi, owner, comment, hidden):
        return cls(identifier=identifier, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url,
                   roi=roi, owner=owner, comment=comment, hidden=hidden)

    def __str__(self):
        return f"{self.id}, {self.identifier}, {self.name}, {self.server.id}, {self.viewer_url}, {self.birdseye_url}, \
                 {self.owner.id}, {self.roi}, {self.comment}, {self.hidden}"

    def __repr__(self):
        return f"{self.id}, {self.identifier}, {self.name}, {self.server.id}, {self.viewer_url}, {self.birdseye_url}, \
                 {self.owner.id}, {self.roi}, {self.comment}, {self.hidden}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def is_omero_image(self):
        if self.server.is_omero547():
            return True
        else:
            return False

    def is_non_omero_image(self):
        if self.server.is_omero547():
            return False
        else:
            return True

    def is_duplicate(self, a_identifier, a_name, a_server, a_viewer_url, a_birdseye_url, a_roi, a_owner, a_comment,
                     a_hidden):

        if self.identifier == a_identifier and self.name == a_name and self.server == a_server and \
           self.viewer_url == a_viewer_url and self.birdseye_url == a_birdseye_url and self.roi == a_roi and \
           self.owner == a_owner and self.comment == a_comment and self.hidden == a_hidden:

            return True
        else:
            return False

    def image_id(self):
        return self.identifier

    def exists_parent_image_links(self):
        return exists_parent_image_links_for_image(self)

    def get_parent_image_links(self):
        return get_parent_image_links_for_image(self)

    def exists_child_image_links(self):
        return exists_child_image_links_for_image(self)

    def get_child_image_links(self):
        return get_child_image_links_for_image(self)

    def exists_image_links(self):

        boolReturn = False

        if exists_parent_image_links_for_image(self) or exists_child_image_links_for_image(self):

            boolReturn = True

        return boolReturn

    def get_file_name_from_birdseye_url(self):

        environment = get_primary_cpw_environment()

        full_web_root = environment.get_full_web_root() + '/'
        web_root_len = len(full_web_root)
        local_image_name = self.birdseye_url[web_root_len:]

        return local_image_name

    def has_tags(self):
        if self.tags.all() is None:
            return False
        else:
            return True

    def get_tags(self):
        return self.tags.all()

    def has_this_tag(self, a_tag):

        tag_present = False

        if self.has_tags():

            tags = self.get_tags()

            for tag in tags:

                if tag == a_tag:

                    tag_present = True

        return tag_present
