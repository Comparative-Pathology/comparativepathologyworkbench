#!/usr/bin/python3
###!
# \file         views_permissions.py
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
# This contains the delete_collection_collection_authorisation view routine
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse

from matrices.models import Collection
from matrices.models import CollectionAuthorisation
from matrices.models import Matrix

from matrices.routines import exists_benches_for_last_used_collection
from matrices.routines import get_benches_for_last_used_collection

#
# DELETE A COLLECTION AUTHORISATION
#
@login_required
def delete_collection_collection_authorisation(request, collection_id, collection_authorisation_id):

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)
    collection = get_object_or_404(Collection, pk=collection_authorisation.collection.id)

    if exists_benches_for_last_used_collection(collection):

        matrix_list = get_benches_for_last_used_collection(collection)

        for matrix in matrix_list:

            if matrix.owner == collection_authorisation.permitted:

                matrix.set_no_last_used_collection()

                matrix.save()

    messages.success(request, 'Collection Authorisation ' + str(collection_authorisation.id) + ' Deleted!')

    collection_authorisation.delete()

    return redirect('list_collection_collection_authorisation', collection_id=collection_id)
