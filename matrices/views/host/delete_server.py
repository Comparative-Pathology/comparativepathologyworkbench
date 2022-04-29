#!/usr/bin/python3
###!
# \file         views_host.py
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
#
# This file contains the delete_server view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Server

from matrices.routines import get_header_data
from matrices.routines import exists_image_for_server

NO_CREDENTIALS = ''

#
# DELETE AN IMAGE SERVER
#
@login_required
def delete_server(request, server_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_owned_by(request.user) or request.user.is_superuser:

            if exists_image_for_server(server):

                messages.error(request, 'CPW_WEB:0700 Server NOT Deleted - Outstanding Images Exist!')

            else:

                messages.success(request, 'Server ' + str(server.id) + ' Deleted!')

                server.delete()

            return HttpResponseRedirect(reverse('list_imaging_hosts', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))
