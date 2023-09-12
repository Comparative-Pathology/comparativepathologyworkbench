#!/usr/bin/python3
###!
# \file         image_list_by_user_and_direction.py
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
# Get All Benches for a particular User
###
from __future__ import unicode_literals

import re

from django.contrib.auth.models import User

from django.apps import apps

from matrices.routines import collection_list_by_user_and_direction
from matrices.routines import get_list_of_image_ids_for_collection_summary


"""
    Get All Images for a particular User
"""


def image_list_by_user_and_direction(a_user,
                                     a_direction,
                                     a_query_name,
                                     a_query_source,
                                     a_query_roi,
                                     a_query_comment,
                                     a_query_hidden,
                                     a_query_owner,
                                     a_query_collection_id,
                                     a_query_matrix_id,
                                     a_query_tag_id):

    # Search Parameters
    search_collection_id = 0
    search_tag_id = 0
    search_bench_id = 0

    if str(a_query_collection_id).isdigit():

        search_collection_id = int(a_query_collection_id)
    
    if str(a_query_tag_id).isdigit():

        search_tag_id = int(a_query_tag_id)

    if str(a_query_matrix_id).isdigit():

        search_bench_id = int(a_query_matrix_id)
    
    ImageSummary = apps.get_model('matrices', 'ImageSummary')
    Collection = apps.get_model('matrices', 'Collection')
    Matrix = apps.get_model('matrices', 'Matrix')
    Server = apps.get_model('matrices', 'Server')
    Tag = apps.get_model('taggit', 'Tag')

    str_query_tag = ''
    str_query_collection = ''
    str_query_matrix = ''
    str_query_source = ''
    str_query_owner = ''

    tag = None

    collection_summary_list = collection_list_by_user_and_direction(a_user, '', '', '', '', '', '')

    list_of_image_ids = get_list_of_image_ids_for_collection_summary(collection_summary_list)

    if search_tag_id != 0:

        tag = Tag.objects.get(pk=int(search_tag_id))
        str_query_tag = str(tag.id)

    if search_collection_id != 0:

        collection = Collection.objects.get(pk=int(search_collection_id))
        str_query_collection = str(collection.id)

    if search_bench_id != 0:

        matrix = Matrix.objects.get(pk=int(a_query_matrix_id))
        str_query_matrix = str(matrix.id)

    if a_query_source != '':

        server = Server.objects.get(pk=int(a_query_source))
        str_query_source = server.name

    if a_query_owner != '':

        user = User.objects.get(pk=int(a_query_owner))
        str_query_owner = user.username

    sort_parameter = 'image_id'

    if a_direction == '':

        sort_parameter = 'image_id'

    else:

        sort_parameter = a_direction

    queryset = []
    queryset_out = []

    str_iregex = ''

    if '*' in a_query_name:

        str_array = a_query_name.split('*')

        for i in range(0, len(str_array)):

            if i == 0:

                str_iregex = re.escape(str_array[i])
        
            else:

                str_iregex = str_iregex + r".*" + re.escape(str_array[i])

    if '*' in a_query_name:

        if a_user.is_superuser:
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .order_by(sort_parameter)
    
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .order_by(sort_parameter)
    
        else:
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__iregex=str_iregex)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
    else:
    
        if a_user.is_superuser:
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .order_by(sort_parameter)
                
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_server=str_query_source)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_server=str_query_source)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_owner=str_query_owner)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '' and str_query_owner == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .order_by(sort_parameter)
    
        else:
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name != '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_name__icontains=a_query_name)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment != '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_comment__icontains=a_query_comment)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi != '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_roi=a_query_roi)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection != '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_collection_id=str_query_collection)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix != '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_matrix_id=str_query_matrix)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source != '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_server=str_query_source)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
            if a_query_name == '' and a_query_comment == '' and a_query_roi == '' and str_query_collection == '' and \
               str_query_matrix == '' and str_query_source == '':
                queryset = ImageSummary.objects.filter(image_hidden=a_query_hidden)\
                    .filter(image_id__in=list_of_image_ids)\
                    .order_by(sort_parameter)
    
    if tag is not None:
            
        for imagesummary in queryset:

            if imagesummary.has_this_tag(tag):

                queryset_out.append(imagesummary)

        queryset = queryset_out

    return queryset