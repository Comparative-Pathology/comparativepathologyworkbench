#!/usr/bin/python3
###!
# \file         activate_in_collection.py
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
# This file contains the activate_collection view routine
#
###
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import SearchUrlForm

from matrices.models import Collection
from matrices.models import CollectionSummary

from matrices.routines import credential_exists
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection


#
# ACTIVATE AN IMAGE COLLECTION on View Collection Page
#
@login_required
def activate_in_collection(request, collection_id):

    if request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied


    if credential_exists(request.user):

        collection = get_object_or_404(Collection, pk=collection_id)

        request.user.profile.set_active_collection(collection)
        request.user.save()

        messages.success(request, 'Collection ' + "{:06d}".format(collection.id) + ' Activated!')

        data = get_header_data(request.user)

        collection = get_object_or_404(Collection, pk=collection_id)

        collection_image_list = get_images_for_collection(collection)

        username = request.user.username
        collection_summary_list_qs = CollectionSummary.objects.raw('SELECT id, collection_id, LAG(\"collection_id\") OVER(ORDER BY \"collection_id\") AS \"prev_val\", LEAD(\"collection_id\") OVER(ORDER BY \"collection_id\" ) AS \"next_val\" FROM public.matrices_collection_summary WHERE collection_authorisation_permitted = %s AND collection_authorisation_authority != \'ADMIN\'', [username])

        next_collection = 0
        previous_collection = 0
        highest_collection = 0
        lowest_collection = 0

        for collection_summary in collection_summary_list_qs:
            if collection_id == collection_summary.collection_id:
                previous_collection = collection_summary.prev_val
                next_collection = collection_summary.next_val

            if collection_summary.prev_val == None:
                lowest_collection = collection_summary.collection_id

            if collection_summary.next_val == None:
                highest_collection = collection_summary.collection_id

        if previous_collection == None:
            previous_collection = highest_collection

        if next_collection == None:
            next_collection = lowest_collection

        form = SearchUrlForm()

        data.update({ 'previous_collection': previous_collection, 'next_collection': next_collection, 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_collection" })

        return render(request, 'matrices/view_collection.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
