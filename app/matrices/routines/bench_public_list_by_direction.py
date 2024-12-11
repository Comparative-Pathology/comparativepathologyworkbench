#!/usr/bin/python3
#
# ##
# \file         bench_public_list_by_direction.py
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
# Get All Public Benches
# ##
#
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User

from django.apps import apps

from django.db.models import Q


#
#   Get All Public Benches
#
def bench_public_list_by_direction(a_direction,
                                   a_query_title,
                                   a_query_description,
                                   a_query_owner,
                                   a_query_created_after,
                                   a_query_created_before,
                                   a_query_modified_after,
                                   a_query_modified_before,
                                   a_query_search_term):

    MatrixPublicSummary = apps.get_model('matrices', 'MatrixPublicSummary')

    str_query_owner = ''

    if a_query_description != '':
        a_query_description = a_query_description

    if a_query_owner != '':
        user = User.objects.get(pk=int(a_query_owner))
        str_query_owner = user.username

    sort_parameter = 'matrix_public_id'

    if a_direction == '':

        sort_parameter = 'matrix_public_id'

    else:

        sort_parameter = a_direction

    queryset = []

    if a_query_search_term == '':

        if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after == '' and \
           a_query_modified_before == '':

            if a_query_title == '' and a_query_description == '' and str_query_owner == '':
                queryset = MatrixPublicSummary.objects.all().order_by(sort_parameter)

            if a_query_title == '' and a_query_description == '' and str_query_owner != '':
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_owner=str_query_owner)\
                    .order_by(sort_parameter)

            if a_query_title == '' and a_query_description != '' and str_query_owner == '':
                queryset = MatrixPublicSummary.objects\
                    .filter(Q(matrix_public_description__icontains=a_query_description))\
                    .order_by(sort_parameter)

            if a_query_title == '' and a_query_description != '' and str_query_owner != '':
                queryset = MatrixPublicSummary.objects\
                    .filter(Q(matrix_public_description__icontains=a_query_description))\
                    .filter(matrix_public_owner=str_query_owner)\
                    .order_by(sort_parameter)

            if a_query_title != '' and a_query_description == '' and str_query_owner == '':
                queryset = MatrixPublicSummary.objects.filter(Q(matrix_public_title__icontains=a_query_title))\
                    .order_by(sort_parameter)

            if a_query_title != '' and a_query_description == '' and str_query_owner != '':
                queryset = MatrixPublicSummary.objects\
                    .filter(Q(matrix_public_title__icontains=a_query_title))\
                    .filter(matrix_public_owner=str_query_owner)\
                    .order_by(sort_parameter)

            if a_query_title != '' and a_query_description != '' and str_query_owner == '':
                queryset = MatrixPublicSummary.objects\
                    .filter(Q(matrix_public_title__icontains=a_query_title) &
                            Q(matrix_public_description__icontains=a_query_description))\
                    .order_by(sort_parameter)

            if a_query_title != '' and a_query_description != '' and str_query_owner != '':
                queryset = MatrixPublicSummary.objects\
                    .filter(Q(matrix_public_title__icontains=a_query_title) &
                            Q(matrix_public_description__icontains=a_query_description))\
                    .filter(matrix_public_owner=str_query_owner)\
                    .order_by(sort_parameter)

        else:

            if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after == '' and \
                   a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .order_by(sort_parameter)

            if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after != '' and \
               a_query_modified_before == '':
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .order_by(sort_parameter)

            if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after != '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .order_by(sort_parameter)

            if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after == '' and \
               a_query_modified_before == '':
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .order_by(sort_parameter)

            if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after == '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .order_by(sort_parameter)

            if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after != '' and \
               a_query_modified_before == '':
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .order_by(sort_parameter)

            if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after != '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')                    
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after == '' and \
               a_query_modified_before == '':
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after == '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after != '' and \
               a_query_modified_before == '':
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after != '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')                    
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after == '' and \
               a_query_modified_before == '':
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after == '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after != '' and \
               a_query_modified_before == '':
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

            if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after != '' and \
               a_query_modified_before != '':
                date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                queryset = MatrixPublicSummary.objects\
                    .filter(matrix_public_modified__lte=date_modified_before)\
                    .filter(matrix_public_modified__gte=date_modified_after)\
                    .filter(matrix_public_created__lte=date_created_before)\
                    .filter(matrix_public_created__gte=date_created_after)\
                    .order_by(sort_parameter)

    else:

        queryset = MatrixPublicSummary.objects\
            .filter((Q(matrix_public_title__icontains=a_query_search_term) |
                     Q(matrix_public_description__icontains=a_query_search_term)))\
            .order_by(sort_parameter)

    return queryset
