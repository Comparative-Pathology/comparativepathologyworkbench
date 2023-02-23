#!/usr/bin/python3
###!
# \file         get_images_for_collection_summary.py
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
# Get the Images from a particular Collection Summary List
###
from __future__ import unicode_literals

import base64, hashlib

from django.apps import apps

from django.db.models import Q

from os import urandom


"""
    Get the Images from a particular Collection Summary List
"""
def get_images_for_collection_summary(a_collection_summary_list):

    Collection = apps.get_model('matrices', 'Collection')

    image_list = list()

    for collection_summary in a_collection_summary_list:

        collection = Collection.objects.get(id=collection_summary.collection_id)

        image_list.extend(collection.images.filter(Q(hidden=False)))

    image_list = list(set(image_list))

    return image_list
