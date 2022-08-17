#!/usr/bin/python3
###!
# \file         bench_delete.py
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
# This file contains the AJAX bench_delete view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image

WORDPRESS_SUCCESS = 'Success!'


#
# DELETE A BENCH
#
@login_required()
def bench_delete(request, bench_id):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    object_id = ''

    serverWordpress = get_primary_wordpress_server()
    credential = get_credential_for_user(request.user)

    matrix = get_object_or_404(Matrix, pk=bench_id)

    oldCells = Cell.objects.filter(matrix=bench_id)

    if credential.has_apppwd():

        if matrix.has_blogpost():

            response = serverWordpress.delete_wordpress_post(credential, matrix.blogpost)

            if response == WORDPRESS_SUCCESS:

                for oldCell in oldCells:

                    if oldCell.has_blogpost():

                        response = serverWordpress.delete_wordpress_post(credential, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "CPW_WEB:0800 Delete Bench - WordPress Error, Contact System Administrator!")

                    if oldCell.has_image():

                        if not exists_collections_for_image(oldCell.image):

                            cell_list = get_cells_for_image(oldCell.image)

                            delete_flag = True

                            for otherCell in cell_list:

                                if otherCell.matrix.id != bench_id:

                                    delete_flag = False

                            if delete_flag == True:

                                image = oldCell.image

                                oldCell.image = None

                                oldCell.save()

                                image.delete()

                object_id = matrix.id

                matrix.delete()

                matrix_id_formatted = "CPW:" + "{:06d}".format(object_id)
                messages.success(request, 'Bench ' + matrix_id_formatted + ' DELETED!')

            else:

                messages.error(request, "CPW_WEB:0810 Delete Bench - WordPress Error, Contact System Administrator!")

    else:

        messages.error(request, "CPW_WEB:0290 DELETE Bench  - No WordPress Credentials, Contact System Administrator!")

    return JsonResponse({'object_id': object_id})
