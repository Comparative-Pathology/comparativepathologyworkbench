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
# This file contains the edit_matrix view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import MatrixForm

from matrices.models import Matrix

from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data

HTTP_POST = 'POST'
NO_CREDENTIALS = ''
WORDPRESS_SUCCESS = 'Success!'

#
# EDIT THE BENCH DETAILS
#
@login_required
def edit_matrix(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() == True or authority.is_none() == True:

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

        else:

            if request.method == HTTP_POST:

                form = MatrixForm(request.POST, instance=matrix)

                if form.is_valid():

                    matrix = form.save(commit=False)

                    if matrix.is_not_high_enough() == True:
                        matrix.set_minimum_height()

                    if matrix.is_not_wide_enough() == True:
                        matrix.set_minimum_width()

                    if matrix.is_too_high() == True:
                        matrix.set_maximum_height()

                    if matrix.is_too_wide() == True:
                        matrix.set_maximum_width()

                    post_id = ''

                    if matrix.has_no_blogpost() == True:

                        credential = get_credential_for_user(request.user)

                        if credential.has_apppwd():

                            returned_blogpost = serverWordpress.post_wordpress_post(credential, matrix.title, matrix.description)

                            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                post_id = returned_blogpost['id']

                            else:

                                messages.error(request, "ERROR: WordPress Error - Contact System Administrator!")
                                form.add_error(None, "ERROR: WordPress Error - Contact System Administrator!")

                                data.update({'form': form, 'matrix': matrix })

                                return render(request, 'matrices/edit_matrix.html', data)


                        matrix.set_blogpost(post_id)

                    matrix.save()

                    matrix_cells = matrix.get_matrix()
                    columns = matrix.get_columns()
                    rows = matrix.get_rows()

                    data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

                    return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

                else:

                    messages.error(request, "Matrix Form is Invalid!")
                    form.add_error(None, "Matrix Form is Invalid!")

                    data.update({'form': form, 'matrix': matrix })

            else:

                form = MatrixForm(instance=matrix)

                data.update({'form': form, 'matrix': matrix })

            return render(request, 'matrices/edit_matrix.html', data)
