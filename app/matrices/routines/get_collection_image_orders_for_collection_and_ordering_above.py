#!/usr/bin/python3
#
# ##
# \file         get_collection_image_orders_for_collection_and_ordering_above.py
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
# Are there CollectionImageOrders for a given Collection, above a supplied Ordering?
# ##
#
from __future__ import unicode_literals

from django.apps import apps


#
#   Return the CollectionImageOrders for a given Collection, above a supplied Ordering
#
def get_collection_image_orders_for_collection_and_ordering_above(a_collection, a_ordering):

    CollectionImageOrder = apps.get_model('matrices', 'CollectionImageOrder')

    return CollectionImageOrder.objects.filter(collection=a_collection)\
        .filter(ordering__gt=a_ordering)
