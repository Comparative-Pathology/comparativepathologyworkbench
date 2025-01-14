#!/usr/bin/python3
#
# ##
# \file         add_cell.py
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
# This file contains the AJAX add_cell view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import MatrixAddCellForm

from matrices.models import Cell
from matrices.models import Credential
from matrices.models import Matrix

from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import is_request_ajax


#
#   Add a Cell
#
@login_required()
def add_cell(request, matrix_id, cell_id):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=matrix_id)

    if not matrix:

        raise PermissionDenied

    if matrix.is_locked():

        raise PermissionDenied

    cell = Cell.objects.get_or_none(id=cell_id)

    if not cell:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            template_name = 'frontend_forms/generic_form_inner.html'

            if request.method == 'POST':

                form = MatrixAddCellForm(data=request.POST)

                if form.is_valid():

                    cd = form.cleaned_data

                    direction = int(cd.get('direction'))

                    # PUSH Right
                    if direction == 1:

                        nextColumn = matrix.get_column_count()
                        rows = matrix.get_rows()

                        for i, row in enumerate(rows):

                            newCell = Cell.create(matrix, "", "", "", nextColumn, i, "", None)

                            newCell.save()

                        matrix.save()

                        shuffleCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate__gte=cell.xcoordinate)\
                                                   .filter(ycoordinate=cell.ycoordinate)

                        for shuffleCell in shuffleCells:

                            shuffleCell.increment_x()

                            if shuffleCell.xcoordinate > matrix.get_max_column():

                                shuffleCell.xcoordinate = cell.xcoordinate

                            shuffleCell.save()

                        messages.success(request, 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' +
                                         + ' Cell Added with Push Right!')

                    # PUSH Down
                    else:

                        nextRow = matrix.get_row_count()
                        columns = matrix.get_columns()

                        for i, column in enumerate(columns):

                            newCell = Cell.create(matrix, "", "", "", i, nextRow, "", None)

                            newCell.save()

                        matrix.save()

                        shuffleCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate=cell.xcoordinate)\
                                                   .filter(ycoordinate__gte=cell.ycoordinate)

                        for shuffleCell in shuffleCells:

                            shuffleCell.increment_y()

                            if shuffleCell.ycoordinate > matrix.get_max_row():

                                shuffleCell.ycoordinate = cell.ycoordinate

                            shuffleCell.save()

                        messages.success(request, 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' +
                                         + ' Cell Added with Push Down!')

            else:

                form = MatrixAddCellForm()
                form.fields['direction'].initial = [1]

            return render(request, template_name, {'form': form, })

    else:

        raise PermissionDenied
