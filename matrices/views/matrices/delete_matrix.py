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
# This file contains the delete_matrix view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import exists_collections_for_image
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data

WORDPRESS_SUCCESS = 'Success!'
NO_CREDENTIALS = ''

#
# DELETE THE BENCH
#
@login_required
def delete_matrix(request, matrix_id):

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

            oldCells = Cell.objects.filter(matrix=matrix_id)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "ERROR: WordPress Error - Contact System Administrator!")
                            form.add_error(None, "ERROR: WordPress Error - Contact System Administrator!")

                            matrix_cells = matrix.get_matrix()
                            columns = matrix.get_columns()
                            rows = matrix.get_rows()

                            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

                            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))



                if oldCell.has_image():

                    if not exists_collections_for_image(oldCell.image):

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()


            if matrix.has_blogpost() == True:

                credential = get_credential_for_user(request.user)

                if credential.has_apppwd():

                    response = serverWordpress.delete_wordpress_post(request.user.username, matrix.blogpost)

                    if response != WORDPRESS_SUCCESS:

                        messages.error(request, "ERROR: WordPress Error - Contact System Administrator!")
                        form.add_error(None, "ERROR: WordPress Error - Contact System Administrator!")

                        matrix_cells = matrix.get_matrix()
                        columns = matrix.get_columns()
                        rows = matrix.get_rows()

                        data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

                        return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


            matrix.delete()

            return HttpResponseRedirect(reverse('list_benches', args=()))
