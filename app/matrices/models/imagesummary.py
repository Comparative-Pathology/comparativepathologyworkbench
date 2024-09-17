#!/usr/bin/python3
#
# ##
# \file         imagesummary.py
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
# The Image Summary Model - for a VIEW not a table ;-)
# ##
#
from __future__ import unicode_literals

from django.db import models

from matrices.models import Image

from taggit.models import Tag

from matrices.routines.exists_parent_image_links_for_image import exists_parent_image_links_for_image
from matrices.routines.exists_child_image_links_for_image import exists_child_image_links_for_image


SERVER_WORDPRESS = 'WORDPRESS'
SERVER_OMERO_547 = 'OMERO_5.4.7'
SERVER_EBI_SCA = 'EBI_SCA'
SERVER_CPW = 'CPW'


#
#   IMAGE SUMMARY (a VIEW for ALL Images)
#
class ImageSummary(models.Model):
    image_id = models.IntegerField(default=0, blank=False)
    image_identifier = models.IntegerField(default=0)
    image_name = models.CharField(max_length=255, blank=False, default='')
    image_viewer_url = models.CharField(max_length=255, blank=False, default='')
    image_birdseye_url = models.CharField(max_length=255, blank=False, default='')
    image_server = models.CharField(max_length=50, blank=False, default='')
    image_server_id = models.IntegerField(default=0, blank=False)
    image_server_url_server = models.CharField(max_length=50, blank=False, default='')
    image_server_uid = models.CharField(max_length=50, blank=True, default='')
    image_server_accesible = models.BooleanField(default=False)
    image_server_type_name = models.CharField(max_length=12, blank=False, unique=True, default='')
    image_roi = models.IntegerField(default=0)
    image_comment = models.TextField(max_length=4095, default='')
    image_hidden = models.BooleanField(default=False)
    image_owner = models.CharField(max_length=50, default='')
    image_collection_id = models.IntegerField(default=0, blank=False)
    image_collection_title = models.CharField(max_length=255, default='')
    image_collection_owner = models.CharField(max_length=50, default='')
    image_matrix_id = models.IntegerField(default=0, blank=False)
    image_matrix_title = models.CharField(max_length=255, default='')
    image_matrix_owner = models.CharField(max_length=50, default='')
    image_tags = models.CharField(max_length=4096, default='')
    image_ordering = models.IntegerField(default=0, blank=False)
    image_ordering_permitted = models.CharField(max_length=50, default='')
    image_ordering_permitted_id = models.IntegerField(default=0, blank=False)

    class Meta:
        managed = False
        db_table = 'matrices_image_summary'

    def __str__(self):
        return f"{self.image_id}, {self.image_identifier}, {self.image_name}, {self.image_viewer_url}, \
                {self.image_birdseye_url}, {self.image_server}, \
                {self.image_server_id}, {self.image_server_url_server}, {self.image_server_uid}, \
                {self.image_server_accesible}, {self.image_server_type_name}, \
                {self.image_roi}, {self.image_comment}, {self.image_hidden}, {self.image_owner}, \
                {self.image_collection_id}, {self.image_collection_title}, {self.image_collection_owner}, \
                {self.image_matrix_id}, {self.image_matrix_title}, {self.image_matrix_owner}, {self.image_tags}, \
                {self.image_ordering}, {self.image_ordering_permitted}, {self.image_ordering_permitted_id}"

    def __repr__(self):
        return f"{self.image_id}, {self.image_identifier}, {self.image_name}, {self.image_viewer_url}, \
                {self.image_birdseye_url}, {self.image_server}, \
                {self.image_server_id}, {self.image_server_url_server}, {self.image_server_uid}, \
                {self.image_server_accesible}, {self.image_server_type_name}, \
                {self.image_roi}, {self.image_comment}, {self.image_hidden}, {self.image_owner}, \
                {self.image_collection_id}, {self.image_collection_title}, {self.image_collection_owner}, \
                {self.image_matrix_id}, {self.image_matrix_title}, {self.image_matrix_owner}, {self.image_tags}, \
                {self.image_ordering}, {self.image_ordering_permitted}, {self.image_ordering_permitted_id}"

    def is_accessible(self):
        if self.image_server_accesible is True:
            return True
        else:
            return False

    def is_not_accessible(self):
        if self.image_server_accesible is False:
            return True
        else:
            return False

    def is_wordpress(self):
        if self.image_server_type_name == SERVER_WORDPRESS:
            return True
        else:
            return False

    def is_omero547(self):
        if self.image_server_type_name == SERVER_OMERO_547:
            return True
        else:
            return False

    def is_ebi_sca(self):
        if self.image_server_type_name == SERVER_EBI_SCA:
            return True
        else:
            return False

    def is_cpw(self):
        if self.image_server_type_name == SERVER_CPW:
            return True
        else:
            return False

    def exists_parent_image_links(self):
        image = Image.objects.get(pk=int(self.image_id))

        return exists_parent_image_links_for_image(image)

    def exists_child_image_links(self):
        image = Image.objects.get(pk=int(self.image_id))

        return exists_child_image_links_for_image(image)

    def has_tags(self):
        if self.image_tags == '':
            return False
        else:
            return True

    def get_tags(self):

        list_of_tag_ids = []

        tag_queryset = None

        if self.image_tags != '':

            tag_array = self.image_tags.split('|')

            for tag in tag_array:

                tag_attribute_array = tag.split(',')

                list_of_tag_ids.append(tag_attribute_array[0])

            tag_queryset = Tag.objects.filter(id__in=list_of_tag_ids).order_by('id')

        return tag_queryset

    def has_this_tag(self, a_tag):

        tag_present = False

        if self.has_tags():

            tag_queryset = self.get_tags()

            for tag in tag_queryset:

                if tag == a_tag:

                    tag_present = True

        return tag_present
