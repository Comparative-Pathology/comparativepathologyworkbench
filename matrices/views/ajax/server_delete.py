#!/usr/bin/python3
###!
# \file         delete_server.py
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
# This file contains the AJAX server_delete view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.models import Server

from matrices.routines import credential_exists


#
# DELETE AN IMAGE SERVER
#
@login_required()
def server_delete(request, server_id):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not request.user.is_superuser:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    server = get_object_by_uuid_or_404(Server, server_id)
    server.delete()

    messages.success(request, 'Server ' + str(server_id) + ' Deleted!')

    return JsonResponse({'object_id': server_id})
