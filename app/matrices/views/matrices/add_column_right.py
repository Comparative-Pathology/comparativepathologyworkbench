#!/usr/bin/python3
###!
# \file         add_column_right.py
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
# This file contains the add_column_right view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_header_data


#
# ADD A COLUMN OF CELLS TO THE RIGHT OF THE GIVEN COLUMN IN THE BENCH
#
@login_required
def add_column_right(request, matrix_id, column_id):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gt=column_id)
            rows = matrix.get_rows()

            for oldcell in oldCells:

                oldcell.increment_x()

                oldcell.save()

            new_column_id = int(column_id) + 1

            for i, row in enumerate(rows):

                cell = Cell.create(matrix, "", "", new_column_id, i, "", None)

                cell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
