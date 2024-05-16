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

from django.apps import apps

from . import bench_list_by_user_and_direction
from . import bench_public_list_by_direction
from . import collection_list_by_user_and_direction
from matrices.routines.get_images_for_collection_summary import get_images_for_collection_summary
from matrices.routines.get_hidden_images_for_collection_summary import get_hidden_images_for_collection_summary
from matrices.routines.get_primary_cpw_environment_summary import get_primary_cpw_environment_summary

SERVER_IDR = 'idr.openmicroscopy.org'


#
#    Get the Data to Populate Base.html (The Header Template)
#
def get_header_data(a_user):

    image_list = list()
    hidden_image_list = list()
    server_list = list()
    matrix_list = list()
    matrix_public_list = list()
    collection_summary_list = list()

    environment_summary = get_primary_cpw_environment_summary()

    if a_user.is_anonymous:

        matrix_public_list = bench_public_list_by_direction('', '', '', '', '', '', '', '', '')

    else:

        Server = apps.get_model('matrices', 'Server')

        if a_user.username == 'guest':

            server_list = Server.objects.filter(url_server=SERVER_IDR).order_by('id')

        else:

            server_list = Server.objects.all().order_by('id')

        matrix_list = bench_list_by_user_and_direction(a_user, '', '', '', '', '', '', '', '', '', '')

        matrix_public_list = bench_public_list_by_direction('', '', '', '', '', '', '', '', '')

        collection_summary_list = collection_list_by_user_and_direction(a_user, '', '', '', '', '', '')

        image_list = get_images_for_collection_summary(collection_summary_list)
        hidden_image_list = get_hidden_images_for_collection_summary(collection_summary_list)

    data = {'environment_summary': environment_summary,
            'collection_list': collection_summary_list,
            'matrix_list': matrix_list,
            'matrix_public_list': matrix_public_list,
            'server_list': server_list,
            'image_list': image_list,
            'hidden_image_list': hidden_image_list}

    return data
