#!/usr/bin/python3
#
# ##
# \file         overwrite_cell.py
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
# This file contains the overwrite_cell view routine - CUT
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image
from matrices.routines import exists_update_for_bench_and_user
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines import is_request_ajax


#
#   OVERWRITE A CELL - MOVE - CUT
#
#    Overwrites Target Cell with Source Cell, Source Cell is emptied - CUT
#
@login_required()
def overwrite_cell(request):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    source = request.POST['source']
    target = request.POST['target']

    source_cell = Cell.objects.get_or_none(id=source)

    if not source_cell:

        raise PermissionDenied

    target_cell = Cell.objects.get_or_none(id=target)

    if not target_cell:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        matrix = source_cell.matrix

        environment = get_primary_cpw_environment()

        if exists_update_for_bench_and_user(matrix, request.user):

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:

                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()

                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            if target_cell.has_blogpost():

                if credential.has_apppwd() and environment.is_wordpress_active():

                    response = environment.delete_a_post_from_wordpress(credential, target_cell.blogpost)

            if target_cell.has_image():

                if exists_collections_for_image(target_cell.image):

                    cell_list = get_cells_for_image(target_cell.image)

                    other_bench_Flag = False

                    for otherCell in cell_list:

                        if otherCell.matrix.id != matrix.id:

                            other_bench_Flag = True

                    if other_bench_Flag is True:

                        if request.user.profile.is_hide_collection_image():

                            target_cell.image.set_hidden(True)
                            target_cell.image.save()

                        else:

                            target_cell.image.set_hidden(False)
                            target_cell.image.save()

                    else:

                        target_cell.image.set_hidden(False)
                        target_cell.image.save()

                else:

                    cell_list = get_cells_for_image(target_cell.image)

                    delete_flag = True

                    for otherCell in cell_list:

                        if otherCell.matrix.id != matrix.id:

                            delete_flag = False

                    if delete_flag is True:

                        image = target_cell.image

                        target_cell.image = None

                        target_cell.save()

                        image.delete()

            source_xcoordinate = source_cell.xcoordinate
            source_ycoordinate = source_cell.ycoordinate

            target_xcoordinate = target_cell.xcoordinate
            target_ycoordinate = target_cell.ycoordinate

            source_cell.xcoordinate = target_xcoordinate
            source_cell.ycoordinate = target_ycoordinate

            target_cell.xcoordinate = source_xcoordinate
            target_cell.ycoordinate = source_ycoordinate

            target_cell.title = ""
            target_cell.description = ""

            target_cell.blogpost = ""
            target_cell.image = None

            source_cell.save()
            target_cell.save()

            data = {'failure': False, 'source': str(source), 'target': str(target)}
            return JsonResponse(data)

        else:

            data = {'failure': True, 'source': str(source), 'target': str(target)}
            return JsonResponse(data)

    else:

        data = {'failure': True, 'source': str(source), 'target': str(target)}
        return JsonResponse(data)
