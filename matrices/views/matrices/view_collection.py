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
# This file contains the view_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matrices.forms import SearchUrlForm

from matrices.models import Collection

from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection

#
# VIEW A COLLECTION
#
@login_required
def view_collection(request, collection_id):

    data = get_header_data(request.user)

    collection = get_object_or_404(Collection, pk=collection_id)

    collection_image_list = get_images_for_collection(collection)

    form = SearchUrlForm()

    data.update({ 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_collection" })

    return render(request, 'matrices/view_collection.html', data)
