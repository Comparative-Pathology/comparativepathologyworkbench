#!/usr/bin/python3
#
# ##
# \file         swap_rows.py
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
# This file contains the swap_rows view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import exists_update_for_bench_and_user
from matrices.routines import is_request_ajax


#
#   SWAP ROWS - SWAP ROW A WITH ROW B
#
@login_required()
def swap_rows(request):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    source = request.POST['source']
    target = request.POST['target']

    in_source_cell = Cell.objects.get_or_none(id=source)

    if not in_source_cell:

        raise PermissionDenied

    in_target_cell = Cell.objects.get_or_none(id=target)

    if not in_target_cell:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        matrix = in_source_cell.matrix

        if exists_update_for_bench_and_user(matrix, request.user):

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

                    cell = Cell.create(matrix, "", "", "", i, nextRow, "", None)

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
