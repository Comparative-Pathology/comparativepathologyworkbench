#!/usr/bin/python3
###!
# \file         add_rows.py
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
# This file contains the AJAX bench_update view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.forms import MatrixAddRowForm

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import get_authority_for_bench_and_user_and_requester


#
# EDIT A BENCH
#
@login_required()
def add_rows(request, matrix_id, row_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if credential_exists(request.user):

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            template_name = 'frontend_forms/generic_form_inner.html'

            if request.method == 'POST':

                form = MatrixAddRowForm(data=request.POST)

                if form.is_valid():

                    cd = form.cleaned_data

                    direction = int(cd.get('direction'))
                    amount = int(cd.get('amount'))

                    if direction == 1:

                        oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gte=row_id)
                        columns = matrix.get_columns()

                        for oldcell in oldCells:

                            oldcell.add_to_y(amount)
                            oldcell.save()

                        max_row_id = int(row_id) + amount
                        new_row_id = int(row_id)

                        for row in range(new_row_id, max_row_id):

                            for i, column in enumerate(columns):

                                cell = Cell.create(matrix, "", "", "", i, row, "", None)
                                cell.save()

                        matrix.save()

                        matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                        messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' + str(amount)
                                         + ' Rows Added Above!')

                    else:

                        oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gt=row_id)
                        columns = matrix.get_columns()

                        for oldcell in oldCells:

                            oldcell.add_to_y(amount)
                            oldcell.save()

                        max_row_id = int(row_id) + amount + 1
                        new_row_id = int(row_id) + 1

                        for row in range(new_row_id, max_row_id):

                            for i, column in enumerate(columns):

                                cell = Cell.create(matrix, "", "", "", i, row, "", None)
                                cell.save()

                        matrix.save()

                        matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                        messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' + str(amount)
                                         + ' Rows Added Below!')

            else:

                form = MatrixAddRowForm()
                form.fields['direction'].initial = [1]

            return render(request, template_name, {
                'form': form,
            })

    else:

        raise PermissionDenied
