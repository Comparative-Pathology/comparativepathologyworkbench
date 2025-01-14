#!/usr/bin/python3
#
# ##
# \file         collection_authorisation_delete.py
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
from matrices.models import CollectionAuthorisation
from matrices.models import CollectionImageOrder
from matrices.models import Credential

from matrices.routines import collection_authorisation_delete_consequences
from matrices.routines import exists_update_for_collection_and_user
from matrices.routines import is_request_ajax


#
#   DELETE A COLLECTION AUTHORISATION
#
@login_required()
def collection_authorisation_delete(request, collection_authorisation_id):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    collection_authorisation = CollectionAuthorisation.objects.get_or_none(id=collection_authorisation_id)

    if not collection_authorisation:

        raise PermissionDenied

    collection = Collection.objects.get_or_none(id=collection_authorisation.collection.id)

    if not collection:

        raise PermissionDenied

    if not exists_update_for_collection_and_user(collection, request.user):

        raise PermissionDenied

    collection_image_ordering_list = CollectionImageOrder.objects.filter(collection=collection)\
                                                                 .filter(permitted=collection_authorisation.permitted)

    for collection_image_ordering in collection_image_ordering_list:

        collection_image_ordering.delete()

    collection_authorisation_delete_consequences(collection_authorisation.permitted, collection)

    messages.success(request, 'Collection Authorisation ' + str(collection_authorisation.id) + ' Deleted!')

    object_id = collection_authorisation.id

    collection_authorisation.delete()

    return JsonResponse({'object_id': object_id})
