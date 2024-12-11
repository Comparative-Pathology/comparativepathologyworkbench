#!/usr/bin/python3
#
# ##
# \file         view_public_matrix.py
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
# This file contains the view_public_matrix view routine
# ##
#
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.models import Matrix

from matrices.routines import get_header_data


#
#   DISPLAY THE PUBLIC BENCH!
#
def view_public_matrix(request, matrix_id):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=matrix_id)

    if not matrix:

        raise PermissionDenied

    data = get_header_data(request.user)

    matrix_cells = matrix.get_matrix()

    columns = matrix.get_columns()
    rows = matrix.get_rows()

    data.update({'matrix': matrix,
                 'rows': rows,
                 'columns': columns,
                 'matrix_cells': matrix_cells})

    return render(request, 'matrices/view_public_matrix.html', data)
