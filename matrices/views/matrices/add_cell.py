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
# This file contains the add_cell view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import get_authority_for_bench_and_user_and_requester

from matrices.routines import get_header_data

NO_CREDENTIALS = ''

#
# ADD A GRID OF CELLS TO A BENCH BENCH
#
@login_required
def add_cell(request, matrix_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = Matrix.objects.get(id=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() == True or authority.is_none() == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            cell_list = Cell.objects.filter(matrix=matrix)

            if not cell_list:

                cell1 = Cell.create(matrix, "", "", 0, 0, "", None)
                cell2 = Cell.create(matrix, "", "", 0, 1, "", None)
                cell3 = Cell.create(matrix, "", "", 0, 2, "", None)
                cell4 = Cell.create(matrix, "", "", 1, 0, "", None)
                cell5 = Cell.create(matrix, "", "", 1, 1, "", None)
                cell6 = Cell.create(matrix, "", "", 1, 2, "", None)
                cell7 = Cell.create(matrix, "", "", 2, 0, "", None)
                cell8 = Cell.create(matrix, "", "", 2, 1, "", None)
                cell9 = Cell.create(matrix, "", "", 2, 2, "", None)

                cell1.save()
                cell2.save()
                cell3.save()
                cell4.save()
                cell5.save()
                cell6.save()
                cell7.save()
                cell8.save()
                cell9.save()

                matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))
