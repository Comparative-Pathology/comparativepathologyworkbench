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
# This file contains the AJAX collection_authorisation_delete view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from matrices.models import Collection
from matrices.models import Matrix

from matrices.routines import get_images_for_collection
from matrices.routines import get_collections_for_image
from matrices.routines import exists_image_in_cells
from matrices.routines import exists_bench_for_last_used_collection
from matrices.routines import get_benches_for_last_used_collection
from matrices.routines import set_first_active_collection_for_user

from matrices.routines import collection_delete_consequences


#
# DELETE A COLLECTION
#
@login_required()
def collection_delete(request, collection_id):

    collection = get_object_or_404(Collection, pk=collection_id)

    collection_delete_consequences(request.user, collection)

    messages.success(request, 'Collection ' + "{:06d}".format(collection.id) + ' DELETED!')

    object_id = collection.id

    collection.delete()

    return JsonResponse({'object_id': object_id})
