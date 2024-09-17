#!/usr/bin/python3
#
# ##
# \file         get_max_collection_image_ordering_for_collection.py
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
# Get the Maximum ordering for a Particular Collection
# ##
#
from __future__ import unicode_literals

from django.apps import apps

from django.db.models import Max


#
#   Count the Collections for a particular User
#
def get_max_collection_image_ordering_for_collection(a_collection_id):

    CollectionImageOrder = apps.get_model('matrices', 'CollectionImageOrder')

    max_ordering = 0

    cio_qs = CollectionImageOrder.objects.values("collection_id")\
        .annotate(Max("ordering"))\
        .order_by("collection_id")\
        .filter(collection_id=a_collection_id)

    for cio_summary in cio_qs:

        max_ordering = cio_summary.get("ordering__max")

    return max_ordering
