#!/usr/bin/python3
###!
# \file         view_active_collection.py
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
# This file contains the view_active_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

from matrices.forms import SearchUrlForm

from matrices.models import CollectionSummary

from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection
from matrices.routines import get_hidden_images_for_collection


#
# VIEW THE ACTIVE COLLECTION
#
@login_required
def view_active_collection(request):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        form = SearchUrlForm()

        if exists_active_collection_for_user(request.user):

            collection = get_active_collection_for_user(request.user)

            collection_image_list = get_images_for_collection(collection)
            collection_hidden_image_list = get_hidden_images_for_collection(collection)

            username = request.user.username
            collection_summary_list_qs = CollectionSummary.objects.raw('SELECT id, collection_id, LAG(\"collection_id\") OVER(ORDER BY \"collection_id\") AS \"prev_val\", LEAD(\"collection_id\") OVER(ORDER BY \"collection_id\" ) AS \"next_val\" FROM public.matrices_collection_summary WHERE collection_authorisation_permitted = %s AND collection_authorisation_authority != \'ADMIN\'', [username])

            next_collection = 0
            previous_collection = 0
            highest_collection = 0
            lowest_collection = 0

            for collection_summary in collection_summary_list_qs:
                if collection.id == collection_summary.collection_id:
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

            data.update({ 'previous_collection': previous_collection, 'next_collection': next_collection, 'collection': collection, \
                        'collection_image_list': collection_image_list, 'collection_hidden_image_list': collection_hidden_image_list, 'form': form, \
                        'search_from': "view_active_collection" })

            return render(request, 'matrices/view_collection.html', data)

        else:

            messages.error(request, "CPW_WEB:0590 View Active Collection - You have no Active Image Collection; Please create a Collection!")

            data.update({ 'form': form, 'search_from': "view_all_collections" })

            return render(request, 'matrices/view_all_collections.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
