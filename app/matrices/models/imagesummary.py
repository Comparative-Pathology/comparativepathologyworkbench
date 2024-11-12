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

from django.apps import apps
from django.db import models

from matrices.models import Image

from taggit.models import Tag

from matrices.routines.exists_parent_image_links_for_image import exists_parent_image_links_for_image
from matrices.routines.exists_child_image_links_for_image import exists_child_image_links_for_image


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
    image_roi = models.IntegerField(default=0)
    image_comment = models.TextField(max_length=4095, default='')
    image_hidden = models.BooleanField(default=False)
    image_owner = models.CharField(max_length=50, default='')
    image_ordering = models.IntegerField(default=0, blank=False)
    image_ordering_permitted = models.CharField(max_length=50, default='')
    image_ordering_permitted_id = models.IntegerField(default=0, blank=False)
    image_server_id = models.IntegerField(default=0, blank=False)
    image_collection_ids = models.CharField(max_length=255, blank=False, default='')
    image_matrix_ids = models.CharField(max_length=255, blank=False, default='')
    image_tag_ids = models.CharField(max_length=255, blank=False, default='')

    class Meta:
        managed = False
        db_table = 'matrices_image_summary'

    def __str__(self):
        return f"{self.image_id}, \
                {self.image_identifier}, \
                {self.image_name}, \
                {self.image_viewer_url}, \
                {self.image_birdseye_url}, \
                {self.image_server}, \
                {self.image_roi}, \
                {self.image_comment}, \
                {self.image_hidden}, \
                {self.image_owner}, \
                {self.image_ordering}, \
                {self.image_ordering_permitted}, \
                {self.image_ordering_permitted_id}, \
                {self.image_server_id}, \
                {self.image_collection_ids}, \
                {self.image_matrix_ids}, \
                {self.image_tag_ids}"

    def __repr__(self):
        return f"{self.image_id}, \
                {self.image_identifier}, \
                {self.image_name}, \
                {self.image_viewer_url}, \
                {self.image_birdseye_url}, \
                {self.image_server}, \
                {self.image_roi}, \
                {self.image_comment}, \
                {self.image_hidden}, \
                {self.image_owner}, \
                {self.image_ordering}, \
                {self.image_ordering_permitted}, \
                {self.image_ordering_permitted_id}, \
                {self.image_server_id}, \
                {self.image_collection_ids}, \
                {self.image_matrix_ids}, \
                {self.image_tag_ids}"

    def exists_parent_image_links(self):
        image = Image.objects.get(pk=int(self.image_id))

        return exists_parent_image_links_for_image(image)

    def exists_child_image_links(self):
        image = Image.objects.get(pk=int(self.image_id))

        return exists_child_image_links_for_image(image)

    def has_tags(self):
        if self.image_tag_ids == '':
            return False
        else:
            return True

    def get_tags(self):

        list_of_tag_ids = []

        tag_queryset = None

        if self.image_tag_ids != '':

            tag_id_array = self.image_tag_ids.split('|')

            for tag_id in tag_id_array:

                list_of_tag_ids.append(tag_id)

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

    def has_collections(self):
        if self.image_collection_ids == '':
            return False
        else:
            return True

    def get_collections(self):

        Collection = apps.get_model('matrices', 'Collection')

        list_of_collection_ids = []

        collection_queryset = None

        if self.image_collection_ids != '':

            collection_id_array = self.image_collection_ids.split('|')

            for collection_id in collection_id_array:

                list_of_collection_ids.append(collection_id)

            collection_queryset = Collection.objects.filter(id__in=list_of_collection_ids).order_by('id')

        return collection_queryset

    def has_this_collection(self, a_collection):

        collection_present = False

        if self.has_collections():

            collection_queryset = self.get_collections()

            for collection in collection_queryset:

                if collection == a_collection:

                    collection_present = True

        return collection_present

    def has_matrices(self):
        if self.image_matrix_ids == '':
            return False
        else:
            return True

    def get_matrices(self):

        Matrix = apps.get_model('matrices', 'Matrix')

        list_of_matrix_ids = []

        matrix_queryset = None

        if self.image_matrix_ids != '':

            matrix_id_array = self.image_matrix_ids.split('|')

            for matrix_id in matrix_id_array:

                list_of_matrix_ids.append(matrix_id)

            matrix_queryset = Matrix.objects.filter(id__in=list_of_matrix_ids).order_by('id')

        return matrix_queryset

    def has_this_matrix(self, a_matrix):

        matrix_present = False

        if self.has_matrices():

            matrix_queryset = self.get_matrices()

            for matrix in matrix_queryset:

                if matrix == a_matrix:

                    matrix_present = True

        return matrix_present

    def get_server(self):

        Server = apps.get_model('matrices', 'Server')

        server = Server.objects.get(pk=int(self.image_server_id))

        return server

    def is_wordpress(self):

        server = self.get_server()

        return server.is_wordpress()

    def is_omero547(self):

        server = self.get_server()

        return server.is_omero547()

    def is_ebi_sca(self):

        server = self.get_server()

        return server.is_ebi_sca()

    def is_cpw(self):

        server = self.get_server()

        return server.is_cpw()
