#!/usr/bin/python3
###!
# \file         views_ajax.py
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
# This file contains the import_image view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from matrices.models import Cell
from matrices.models import Image

from matrices.routines import credential_exists
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import exists_update_for_bench_and_user

WORDPRESS_SUCCESS = 'Success!'


#
# IMPORT AN IMAGE FROM BASKET TO CELL - IMPORT
#
@login_required()
def import_image(request):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    source = request.POST['source']
    target = request.POST['target']
    source_type = request.POST['source_type']

    source_image = get_object_or_404(Image, pk=source)
    target_cell = get_object_or_404(Cell, pk=target)

    matrix = target_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    serverWordpress = get_primary_wordpress_server()

    if credential_exists(user):

        if exists_update_for_bench_and_user(matrix, request.user):

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:

                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()

                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            post_id = ''

            target_cell.title = source_image.name
            target_cell.description = source_image.name

            target_cell.image = source_image

            if target_cell.has_no_blogpost():

                credential = get_credential_for_user(request.user)

                if credential.has_apppwd():

                    returned_blogpost = serverWordpress.post_wordpress_post(credential, target_cell.title, target_cell.description)

                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                        post_id = returned_blogpost['id']

                target_cell.set_blogpost(post_id)

            target_cell.save()

            data = { 'failure': False, 'source': str(source), 'target': str(target) }
            return JsonResponse(data)

        else:

            data = { 'failure': True, 'source': str(source), 'target': str(target) }
            return JsonResponse(data)

    else:

        data = { 'failure': True, 'source': str(source), 'target': str(target) }
        return JsonResponse(data)
