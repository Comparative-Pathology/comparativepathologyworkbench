#!/usr/bin/python3
#
# ##
# \file         collection_delete.py
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
# This file contains the AJAX collection_authorisation_delete view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from matrices.models import Collection
from matrices.models import Credential

from matrices.routines import collection_delete_consequences


#
#   DELETE A COLLECTION
#
@login_required()
def collection_delete(request, collection_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    collection = Collection.objects.get_or_none(id=collection_id)

    if not collection:

        raise PermissionDenied

    if collection.is_locked():

        raise PermissionDenied

    object_id = collection.id

    collection_delete_flag = collection_delete_consequences(request.user, collection)

    if collection_delete_flag is True:

        messages.success(request, 'Collection ' + collection.get_formatted_id() + ' DELETED!')

        collection.delete()

    else:

        messages.error(request, 'Collection ' + collection.get_formatted_id() + ' NOT Deleted!')

    return JsonResponse({'object_id': object_id})
