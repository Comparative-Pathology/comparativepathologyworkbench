#!/usr/bin/python3
#
# ##
# \file         delete_this_column.py
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
# This file contains the delete_this_column view routine
# ##
#
from __future__ import unicode_literals

import subprocess

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Credential
from matrices.models import Cell

from matrices.routines import exists_collections_for_image
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_cells_for_image
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines import get_header_data


#
#   DELETE THE GIVEN COLUMN IN THE BENCH
#
@login_required
def delete_this_column(request, matrix_id, column_id):

    matrix = Matrix.objects.get_or_none(id=matrix_id)

    if matrix:

        credential = Credential.objects.get_or_none(username=request.user.username)

        if credential:

            environment = get_primary_cpw_environment()

            data = get_header_data(request.user)

            authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

            if authority.is_viewer() or authority.is_none():

                return HttpResponseRedirect(reverse('home', args=()))

            else:

                matrix = Matrix.objects.get(id=matrix_id)

                deleteColumn = int(column_id)

                oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)

                for oldCell in oldCells:

                    if oldCell.has_blogpost():

                        if credential.has_apppwd() and environment.is_wordpress_active():

                            response = environment.delete_a_post_from_wordpress(credential, oldCell.blogpost)

                    if oldCell.has_image():

                        if exists_collections_for_image(oldCell.image):

                            cell_list = get_cells_for_image(oldCell.image)

                            other_bench_Flag = False

                            for otherCell in cell_list:

                                if otherCell.matrix.id != matrix.id:

                                    other_bench_Flag = True

                            if other_bench_Flag is True:

                                if request.user.profile.is_hide_collection_image():

                                    oldCell.image.set_hidden(True)
                                    oldCell.image.save()

                                else:

                                    oldCell.image.set_hidden(False)
                                    oldCell.image.save()

                            else:

                                oldCell.image.set_hidden(False)
                                oldCell.image.save()

                        else:

                            cell_list = get_cells_for_image(oldCell.image)

                            delete_flag = True

                            for otherCell in cell_list:

                                if otherCell.matrix.id != matrix_id:

                                    delete_flag = False

                            if delete_flag is True:

                                image = oldCell.image

                                oldCell.image = None

                                oldCell.save()

                                if image.server.is_ebi_sca() or image.server.is_cpw():

                                    image_path = environment.document_root + '/' + image.name

                                    rm_command = 'rm ' + str(image_path)
                                    rm_escaped = rm_command.replace("(", "\(").replace(")", "\)")

                                    process = subprocess.Popen(rm_escaped,
                                                               shell=True,
                                                               stdout=subprocess.PIPE,
                                                               stderr=subprocess.PIPE,
                                                               universal_newlines=True)

                                if image.server.is_omero547() and not image.server.is_idr():

                                    image_path = environment.document_root + '/' +\
                                        image.get_file_name_from_birdseye_url()

                                    rm_command = 'rm ' + str(image_path)
                                    rm_escaped = rm_command.replace("(", "\(").replace(")", "\)")

                                    process = subprocess.Popen(rm_escaped,
                                                               shell=True,
                                                               stdout=subprocess.PIPE,
                                                               stderr=subprocess.PIPE,
                                                               universal_newlines=True)

                                image.delete()

                Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()

                moveCells = Cell.objects.filter(matrix=matrix_id, xcoordinate__gt=deleteColumn)

                for moveCell in moveCells:

                    moveCell.decrement_x()

                    moveCell.save()

                matrix.save()

                matrix_cells = matrix.get_matrix()
                columns = matrix.get_columns()
                rows = matrix.get_rows()

                data.update({'matrix': matrix,
                             'rows': rows,
                             'columns': columns,
                             'matrix_cells': matrix_cells})

                return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
