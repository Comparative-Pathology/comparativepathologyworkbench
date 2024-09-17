#!/usr/bin/python3
#
# ##
# \file         collectionsummary.py
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
# The Collection Summary Model - for a VIEW not a table ;-)
# ##
#
from __future__ import unicode_literals

from django.db import models


#
#   The Collection Summary Model (a VIEW for ALL Collections)
#
class CollectionSummary(models.Model):

    collection_id = models.IntegerField(default=0,
                                        blank=False)
    collection_title = models.CharField(max_length=255,
                                        default='')
    collection_description = models.TextField(max_length=4095,
                                              default='')
    collection_owner = models.CharField(max_length=50,
                                        default='')
    collection_image_count = models.IntegerField(default=0,
                                                 blank=False)
    collection_authorisation_id = models.IntegerField(default=0,
                                                      blank=False)
    collection_authorisation_permitted = models.CharField(max_length=50,
                                                          default='')
    collection_authorisation_authority = models.CharField(max_length=12,
                                                          default='')

    class Meta:
        managed = False
        db_table = 'matrices_collection_summary'

    def __str__(self):
        return f"{self.collection_id}, {self.collection_title}, {self.collection_description}, \
            {self.collection_owner}, {self.collection_description}, {self.collection_image_count}, \
            {self.collection_authorisation_permitted}, {self.collection_authorisation_authority}"

    def __repr__(self):
        return f"{self.collection_id}, {self.collection_title}, {self.collection_description}, \
            {self.collection_owner}, {self.collection_description}, {self.collection_image_count}, \
            {self.collection_authorisation_permitted}, {self.collection_authorisation_authority}"
