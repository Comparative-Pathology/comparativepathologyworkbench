#!/usr/bin/python3
###!
# \file         get_header_data.py
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
# Get the Data to Populate Base.html (The Header Template)
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.shortcuts import get_object_or_404

from django.apps import apps

from . import bench_list_by_user_and_direction
from . import credential_exists
from . import collection_list_by_user_and_direction
from matrices.routines.get_images_for_collection_summary import get_images_for_collection_summary


"""
    Get the Data to Populate Base.html (The Header Template)
"""
def get_header_data(a_user):

    Collection = apps.get_model('matrices', 'Collection')

    image_list = list()
    server_list = list()
    matrix_list = list()
    collection_list = list()
    collection_summary_list = list()

    if not a_user.is_anonymous:

        Server = apps.get_model('matrices', 'Server')
        server_list = Server.objects.all().order_by('id')

        matrix_list = bench_list_by_user_and_direction(a_user, '', '', '', '', '', '', '', '', '', '')

        collection_summary_list = collection_list_by_user_and_direction(a_user, '', '', '', '', '')

        image_list = get_images_for_collection_summary(collection_summary_list)


    data = { 'collection_list': collection_summary_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }

    return data
