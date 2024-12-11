#!/usr/bin/python3
# 
# ##
# \file         list_global.py
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
# This file contains the list_imaging_hosts view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Credential

from matrices.routines import get_header_data
from matrices.routines import bench_list_by_user_and_direction
from matrices.routines import collection_list_by_user_and_direction
from matrices.routines import image_list_by_user_and_direction
from matrices.routines import get_primary_cpw_environment


#
#   LIST SERVERS
#
@login_required
def list_global(request):

    readBoolean = False

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        data = get_header_data(request.user)

        environment = get_primary_cpw_environment()

        readBoolean = True

        query_search = request.GET.get('search', '')
        sort_parameter = 'matrix_id'

        bench_list = bench_list_by_user_and_direction(request.user,
                                                      sort_parameter,
                                                      '', '', '', '', '', '', '', '',
                                                      query_search)

        sort_parameter = 'collection_id'

        collection_list = collection_list_by_user_and_direction(request.user,
                                                                sort_parameter,
                                                                '', '', '', '',
                                                                query_search)

        sort_parameter = 'image_name'

        image_list = image_list_by_user_and_direction(request.user,
                                                      sort_parameter,
                                                      query_search,
                                                      '', '', '',
                                                      False,
                                                      '', '', '', '')

        data.update({'search_term': query_search,
                     'search_bench_list': bench_list,
                     'search_collection_list': collection_list,
                     'search_image_list': image_list,
                     'readBoolean': readBoolean,
                     'date_format': environment.date_format})

        return render(request, 'host/list_global.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
