#!/usr/bin/python3
###!
# \file         renumber_bench.py
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
# This file contains the renumber_bench view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Matrix

from matrices.routines import credential_exists

from matrices.routines import Base26


#
#   Renumber the Headings in a Bench
#
@login_required
def renumber_bench(request, bench_id):

    if credential_exists(request.user):

        bench = get_object_or_404(Matrix, pk=bench_id)

        max_row_index = bench.get_max_row()
        max_column_index = bench.get_max_column()

        row_header_cells = bench.get_row_header_cells()
        column_header_cells = bench.get_column_header_cells()

        row = 0
        title_label = ''

        for row_header_cell in row_header_cells:

            if row_header_cell.ycoordinate > 0:

                if row < max_row_index:

                    title_label = str(row)

                    row_header_cell.title = title_label

                    row_header_cell.save()

            row = row + 1

        column = 0
        title_label = ''

        for column_header_cell in column_header_cells:

            if column_header_cell.xcoordinate > 0:

                if column < max_column_index:

                    title_label = Base26.to_excel(column)

                    column_header_cell.title = title_label

                    column_header_cell.save()

            column = column + 1

        matrix_id_formatted = "CPW:" + "{:06d}".format(bench.id)
        messages.success(request, 'Bench ' + matrix_id_formatted + ' Headers Renumbered')

        return HttpResponseRedirect(reverse('matrix', args=(bench_id,)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
