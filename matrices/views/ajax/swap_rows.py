#!/usr/bin/python3
###!
# \file         views_ajax.py
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
# This file contains the swap_rows view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import get_authority_for_bench_and_user_and_requester

#
# SWAP ROWS - SWAP ROW A WITH ROW B
#
@login_required()
def swap_rows(request):
    """
    AJAX - Swap Rows
    """

    source = request.POST['source']
    target = request.POST['target']

    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)

    matrix = in_source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            data = { 'failure': True, 'source': str(source), 'target': str(target) }

            return JsonResponse(data)

        else:

            source_row_cells = matrix.get_row(in_source_cell.ycoordinate)
            target_row_cells = matrix.get_row(in_target_cell.ycoordinate)

            source_ycoordinate = in_source_cell.ycoordinate
            target_ycoordinate = in_target_cell.ycoordinate

            output_cells = list()

            for target_cell in target_row_cells:

                target_cell.set_ycoordinate(source_ycoordinate)

                output_cells.append(target_cell)

            for source_cell in source_row_cells:

                source_cell.set_ycoordinate(target_ycoordinate)

                output_cells.append(source_cell)

            for output_cell in output_cells:

                output_cell.save()


            if matrix.get_max_row() == in_target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()


            data = { 'failure': False, 'source': str(source), 'target': str(target) }

            return JsonResponse(data)

    else:

            data = { 'failure': True, 'source': str(source), 'target': str(target) }

            return JsonResponse(data)
