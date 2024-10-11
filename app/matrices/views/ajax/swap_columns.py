#!/usr/bin/python3
###!
# \file         swap_columns.py
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
# This file contains the swap_columns view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import exists_update_for_bench_and_user

#
# SWAP COLUMNS - SWAP COLUMN A WITH COLUMN B
#
@login_required()
def swap_columns(request):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied

    source = request.POST['source']
    target = request.POST['target']

    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)

    matrix = in_source_cell.matrix

    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        if exists_update_for_bench_and_user(matrix, request.user):

            source_column_cells = matrix.get_column(in_source_cell.xcoordinate)
            target_column_cells = matrix.get_column(in_target_cell.xcoordinate)

            source_xcoordinate = in_source_cell.xcoordinate
            target_xcoordinate = in_target_cell.xcoordinate

            output_cells = list()

            for target_cell in target_column_cells:

                target_cell.set_xcoordinate(source_xcoordinate)

                output_cells.append(target_cell)

            for source_cell in source_column_cells:

                source_cell.set_xcoordinate(target_xcoordinate)

                output_cells.append(source_cell)

            for output_cell in output_cells:

                output_cell.save()

            if matrix.get_max_column() == in_target_cell.xcoordinate:

                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()

                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            data = {'failure': False, 'source': str(source), 'target': str(target)}
            return JsonResponse(data)

        else:

            data = {'failure': True, 'source': str(source), 'target': str(target)}
            return JsonResponse(data)

    else:

        data = {'failure': True, 'source': str(source), 'target': str(target)}
        return JsonResponse(data)
