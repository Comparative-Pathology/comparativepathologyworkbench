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
# This file contains the delete_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Collection

from matrices.routines import exists_bench_for_last_used_collection
from matrices.routines import exists_image_in_cells
from matrices.routines import get_benches_for_last_used_collection
from matrices.routines import get_images_for_collection
from matrices.routines import get_collections_for_image
from matrices.routines import get_header_data
from matrices.routines import set_first_active_collection_for_user

NO_CREDENTIALS = ''

#
# DELETE AN IMAGE COLLECTION
#
@login_required
def delete_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        images = get_images_for_collection(collection)

        for image in images:

            collection_list = get_collections_for_image(image)

            delete_flag = False

            for collection_other in collection_list:

                if collection != collection_other:

                    delete_flag = True

            if delete_flag == False:

                if not exists_image_in_cells(image):

                    Collection.unassign_image(image, collection)

                    image.delete()


        if exists_bench_for_last_used_collection(collection):

            matrix_list = get_benches_for_last_used_collection(collection)

            for matrix in matrix_list:

                matrix.set_no_last_used_collection()

                matrix.save()


        if collection.is_active():

            set_first_active_collection_for_user(request.user)


        messages.success(request, 'Collection ' + "{:06d}".format(collection.id) + ' DELETED!')

        collection.delete()

        return HttpResponseRedirect(reverse('list_collections', args=()))
