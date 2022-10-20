#!/usr/bin/python3
###!
# \file         view_matrix.py
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
# This file contains the view_matrix view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import MatrixSummary

from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_read_for_bench_and_user
from matrices.routines import exists_update_for_bench_and_user
from matrices.routines import get_active_collection_images_for_user
from matrices.routines import get_credential_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection


#
# DISPLAY THE BENCH!
#
@login_required
def view_matrix(request, matrix_id):

    if request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied


    if credential_exists(request.user):

        data = get_header_data(request.user)

        matrix = get_object_or_404(Matrix, pk=matrix_id)
        owner = get_object_or_404(User, pk=matrix.owner_id)
        user = get_object_or_404(User, pk=request.user.id)

        readBoolean = False

        if exists_read_for_bench_and_user(matrix, user):

            readBoolean = True

            view_matrix = 'view_matrix'

            credential = get_credential_for_user(request.user)

            if not credential.has_apppwd():

                matrix_link = ''

            collection_image_list = list()

            if matrix.has_last_used_collection():

                collection_image_list = get_images_for_collection(matrix.last_used_collection)

            else:

                if exists_active_collection_for_user(request.user):

                    collection_image_list = get_active_collection_images_for_user(request.user)

            updateBoolean = False

            if exists_update_for_bench_and_user(matrix, user):

                updateBoolean = True

            matrix_cells = matrix.get_matrix()

            columns = matrix.get_columns()
            rows = matrix.get_rows()

            username = request.user.username
            matrix_summary_list_qs = MatrixSummary.objects.raw('SELECT id, matrix_id, LAG(\"matrix_id\") OVER(ORDER BY \"matrix_id\") AS \"prev_val\", LEAD(\"matrix_id\") OVER(ORDER BY \"matrix_id\" ) AS \"next_val\" FROM public.matrices_bench_summary WHERE matrix_authorisation_permitted = %s AND matrix_authorisation_authority != \'ADMIN\'', [username])

            if username == 'admin':

                matrix_summary_list_qs = MatrixSummary.objects.raw('SELECT id, matrix_id, LAG(\"matrix_id\") OVER(ORDER BY \"matrix_id\") AS \"prev_val\", LEAD(\"matrix_id\") OVER(ORDER BY \"matrix_id\" ) AS \"next_val\" FROM public.matrices_bench_summary WHERE matrix_authorisation_authority = \'OWNER\'')


            next_bench = 0
            previous_bench = 0
            highest_bench = 0
            lowest_bench = 0

            for matrix_summary in matrix_summary_list_qs:
                if matrix_id == matrix_summary.matrix_id:
                    previous_bench = matrix_summary.prev_val
                    next_bench = matrix_summary.next_val

                if matrix_summary.prev_val == None:
                    lowest_bench = matrix_summary.matrix_id

                if matrix_summary.next_val == None:
                    highest_bench = matrix_summary.matrix_id

            if previous_bench == None:
                previous_bench = highest_bench

            if next_bench == None:
                next_bench = lowest_bench

            data.update({ 'previous_bench': previous_bench, 'next_bench': next_bench, 'collection_image_list': collection_image_list, 'view_matrix': view_matrix, 'readBoolean': readBoolean, 'updateBoolean': updateBoolean, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return render(request, 'matrices/view_matrix.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        raise PermissionDenied
