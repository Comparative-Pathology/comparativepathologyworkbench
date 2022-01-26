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
# This file contains the choose_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Collection

from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_header_data
from matrices.routines import set_inactive_collection_for_user

NO_CREDENTIALS = ''

VIEW_MATRIX = "view_matrix"
AMEND_CELL = "amend_cell"

#
# CHOOSE AN IMAGE COLLECTION
#
@login_required
def choose_collection(request, matrix_id, cell_id, collection_id, path_from):

    data = get_header_data(request.user)

    collection_image_list = list()

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)
        owner = get_object_or_404(User, pk=matrix.owner_id)
        user = get_object_or_404(User, pk=request.user.id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, user)

        if authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        collection = get_object_or_404(Collection, pk=collection_id)

        if collection.is_inactive():

            collection.set_active()

            if exists_active_collection_for_user(request.user):

                set_inactive_collection_for_user(request.user)

            collection.save()

        matrix.set_last_used_collection(collection)

        matrix.save()

        if path_from == VIEW_MATRIX:

            return redirect('matrix', matrix_id=matrix_id)

        if path_from == AMEND_CELL:

            return redirect('amend_cell', matrix_id=matrix_id, cell_id=cell_id)

        return redirect('matrix', matrix_id=matrix_id)
