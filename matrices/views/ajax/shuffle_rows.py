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
# This file contains the shuffle_rows view routine
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
# SHUFFLE ROWS - MOVE ROW AND PUSH EXISTING ROWS TO LEFT OR RIGHT
#
@login_required()
def shuffle_rows(request):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    source = request.POST['source']
    target = request.POST['target']

    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)

    source_ycoordinate = in_source_cell.ycoordinate
    target_ycoordinate = in_target_cell.ycoordinate

    matrix = in_source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        if exists_update_for_bench_and_user(matrix, request.user):

            source_row_cells = matrix.get_row(source_ycoordinate)

            if source_ycoordinate < target_ycoordinate:

                oldCells = Cell.objects.filter(matrix=matrix.id).filter(ycoordinate__gt=source_ycoordinate).filter(ycoordinate__lte=target_ycoordinate)

                output_cells = list()

                for oldcell in oldCells:

                    oldcell.decrement_y()

                    output_cells.append(oldcell)

                for source_cell in source_row_cells:

                    source_cell.set_ycoordinate(target_ycoordinate)

                    output_cells.append(source_cell)

                for output_cell in output_cells:

                    output_cell.save()


            if source_ycoordinate > target_ycoordinate:

                oldCells = Cell.objects.filter(matrix=matrix.id).filter(ycoordinate__gte=target_ycoordinate).filter(ycoordinate__lt=source_ycoordinate)

                output_cells = list()

                for oldcell in oldCells:

                    oldcell.increment_y()

                    output_cells.append(oldcell)

                for source_cell in source_row_cells:

                    source_cell.set_ycoordinate(target_ycoordinate)

                    output_cells.append(source_cell)

                for output_cell in output_cells:

                    output_cell.save()


            if matrix.get_max_row() == target_ycoordinate:

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

    else:

        data = { 'failure': True, 'source': str(source), 'target': str(target) }
        return JsonResponse(data)
