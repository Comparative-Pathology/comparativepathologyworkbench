#!/usr/bin/python3
#
# ##
# \file         swap_bench_headers.py
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
# ##
#
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
#   Swap the Headings in a Bench
#
@login_required
def swap_bench_headers(request, bench_id):

    if credential_exists(request.user):

        bench = get_object_or_404(Matrix, pk=bench_id)

        max_row_index = bench.get_max_row()
        max_column_index = bench.get_max_column()

        row_header_cells = bench.get_row_header_cells()
        column_header_cells = bench.get_column_header_cells()

        row = 0
        title_label = ''
        row_comment_flag = False
        column_comment_flag = False

        for row_header_cell in row_header_cells:

            if row_header_cell.ycoordinate > 0:

                if row < max_row_index:

                    title_label = str(row)

                    if row_header_cell.comment == title_label:

                        row_comment_flag = True

                    if row_comment_flag is True:

                        row_header_cell.comment = row_header_cell.title
                        row_header_cell.title = title_label

                    else:

                        row_header_cell.title = row_header_cell.comment
                        row_header_cell.comment = title_label

                    row_header_cell.save()

            row = row + 1

        column = 0
        title_label = ''

        for column_header_cell in column_header_cells:

            if column_header_cell.xcoordinate > 0:

                if column < max_column_index:

                    title_label = Base26.to_excel(column)

                    if column_header_cell.comment == title_label:

                        column_comment_flag = True

                    if column_comment_flag is True:

                        column_header_cell.comment = column_header_cell.title
                        column_header_cell.title = title_label

                    else:

                        column_header_cell.title = column_header_cell.comment
                        column_header_cell.comment = title_label

                    column_header_cell.save()

            column = column + 1

        if column_comment_flag is True and row_comment_flag is True:

            matrix_id_formatted = "CPW:" + "{:06d}".format(bench.id)
            messages.success(request, 'Bench ' + matrix_id_formatted + ' showing Header Numbers!')

        else:

            matrix_id_formatted = "CPW:" + "{:06d}".format(bench.id)
            messages.success(request, 'Bench ' + matrix_id_formatted + ' showing Header Titles!')

        return HttpResponseRedirect(reverse('matrix', args=(bench_id,)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
