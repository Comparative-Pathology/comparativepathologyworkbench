#!/usr/bin/python3
#
# ##
# \file         show_dataset.py
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
# This file contains the show_dataset view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Credential
from matrices.models import Server

from matrices.routines import get_header_data
from matrices.routines import get_primary_cpw_environment


#
#   Show Dataset View routine
#
@login_required()
def show_dataset(request, server_id, dataset_id):

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        image_flag = False

        if request.user.profile.has_active_collection():

            image_flag = True

        data = get_header_data(request.user)

        data.update({'image_flag': image_flag, 'add_from': "show_dataset"})

        server = Server.objects.get_or_none(id=server_id)

        if server:

            if server.is_omero547():

                server_data = {}

                environment = get_primary_cpw_environment()

                if environment.is_web_gateway() or server.is_idr():

                    server_data = server.get_imaging_server_dataset_json(dataset_id, False)

                else:

                    if environment.is_blitz_gateway():

                        server_data = server.get_imaging_server_dataset_json_blitz(dataset_id,
                                                                                   False,
                                                                                   environment.gateway_port)

                data.update(server_data)

                return render(request, 'gallery/show_dataset.html', data)

            else:

                return HttpResponseRedirect(reverse('home', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
