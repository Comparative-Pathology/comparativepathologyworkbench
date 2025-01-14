#!/usr/bin/python3
#
# ##
# \file         server_delete.py
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
# This file contains the AJAX server_delete view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from matrices.models import Credential
from matrices.models import Server

from matrices.routines import exists_image_for_server
from matrices.routines import is_request_ajax


#
#   DELETE AN IMAGE SERVER
#
@login_required()
def server_delete(request, server_id):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    server = Server.objects.get_or_none(id=server_id)

    if server:

        if not request.user.is_superuser:

            if server.owner != request.user:

                raise PermissionDenied

        if exists_image_for_server(server):

            raise PermissionDenied

        server.delete()

    else:

        raise PermissionDenied

    messages.success(request, 'Server ' + str(server_id) + ' Deleted!')

    return JsonResponse({'object_id': server_id})
