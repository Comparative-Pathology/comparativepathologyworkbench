#!/usr/bin/python3
###!
# \file         views_matrices.py
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

from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection

#
# VIEW THE ACTIVE COLLECTION
#
@login_required
def view_active_collection(request):

    data = get_header_data(request.user)

    form = SearchUrlForm()

    if exists_active_collection_for_user(request.user):

        collection_list = get_active_collection_for_user(request.user)

        collection = collection_list[0]

        collection_image_list = get_images_for_collection(collection)

        data.update({ 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_active_collection" })

        return render(request, 'matrices/view_collection.html', data)

    else:

        messages.error(request, "CPW_WEB:0840 View Active Collection - You have no Active Image Collection; Please create a Collection!")

        data.update({ 'form': form, 'search_from': "view_all_collections" })

        return render(request, 'matrices/view_all_collections.html', data)
