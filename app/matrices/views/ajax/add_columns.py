#!/usr/bin/python3
#
# ##
# \file         add_columns.py
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
# This file contains the AJAX bench_update view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import MatrixAddColumnForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import is_request_ajax


#
#   EDIT A BENCH
#
@login_required()
def add_columns(request, matrix_id, column_id):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=matrix_id)

    if not matrix:

        raise PermissionDenied

    if matrix.is_locked():

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            template_name = 'frontend_forms/generic_form_inner.html'

            if request.method == 'POST':

                form = MatrixAddColumnForm(data=request.POST)

                if form.is_valid():

                    cd = form.cleaned_data

                    direction = int(cd.get('direction'))
                    amount = int(cd.get('amount'))

                    if direction == 1:

                        oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gte=column_id)
                        rows = matrix.get_rows()

                        for oldcell in oldCells:

                            oldcell.add_to_x(amount)
                            oldcell.save()

                        max_column_id = int(column_id) + amount
                        new_column_id = int(column_id)

                        for column in range(new_column_id, max_column_id):

                            for i, row in enumerate(rows):

                                cell = Cell.create(matrix, "", "", "", column, i, "", None)
                                cell.save()

                        matrix.save()

                        messages.success(request, 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' + str(amount)
                                         + ' Columns Added to the Left!')

                    else:

                        oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gt=column_id)
                        rows = matrix.get_rows()

                        for oldcell in oldCells:

                            oldcell.add_to_x(amount)
                            oldcell.save()

                        max_column_id = int(column_id) + amount + 1
                        new_column_id = int(column_id) + 1

                        for column in range(new_column_id, max_column_id):

                            for i, row in enumerate(rows):

                                cell = Cell.create(matrix, "", "", "", column, i, "", None)
                                cell.save()

                        matrix.save()

                        messages.success(request, 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' + str(amount)
                                         + ' Columns Added to the Right!')

            else:

                form = MatrixAddColumnForm()
                form.fields['direction'].initial = [1]

            return render(request, template_name, {'form': form, })

    else:

        raise PermissionDenied
