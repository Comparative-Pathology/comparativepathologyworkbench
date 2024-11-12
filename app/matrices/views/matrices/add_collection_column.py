#!/usr/bin/python3
#
# ##
# \file         add_collection_column.py
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
# This file contains the add_collection_column view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Collection
from matrices.models import CollectionImageOrder

from matrices.routines import credential_exists
from matrices.routines import exists_update_for_bench_and_user
from matrices.routines import get_credential_for_user
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines import get_header_data

from background.tasks import add_collection_column_task

WORDPRESS_SUCCESS = 'Success!'


#
#   Add the Selected Collection to this Column
#
@login_required
def add_collection_column(request, matrix_id, column_id):

    environment = get_primary_cpw_environment()

    data = get_header_data(request.user)

    if credential_exists(request.user):

        credential = get_credential_for_user(request.user)

        matrix = Matrix.objects.get(id=matrix_id)

        if exists_update_for_bench_and_user(matrix, request.user):

            if environment.is_background_processing():

                matrix.set_locked()
                matrix.save()

                result = add_collection_column_task.delay_on_commit(request.user.id, matrix.id, column_id)

                #if result.ready():

                #    task_message = result.get(timeout=1)

                matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                messages.error(request, 'Bench ' + matrix_id_formatted + ' LOCKED pending Update!')

            else:

                collection = Collection.objects.get(id=matrix.last_used_collection.id)

                collection_image_count = collection.get_images_count()

                cells = Cell.objects.filter(matrix=matrix_id, xcoordinate=int(column_id)).order_by('ycoordinate')

                cell_count_minus_footer = len(cells) - 1

                free_cell_count = 0

                for cell in cells:

                    if cell.has_image():

                        break

                    else:

                        if not cell.is_header():

                            free_cell_count = free_cell_count + 1

                if free_cell_count == cell_count_minus_footer:

                    # Deduct 1 for the Footer cell only
                    free_cell_count = free_cell_count - 1

                row_id = free_cell_count

                rows_to_add = 0

                if collection_image_count > free_cell_count:

                    # the collection is too big for the available cells
                    rows_to_add = collection_image_count - free_cell_count

                    oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gt=row_id)
                    columns = matrix.get_columns()

                    for oldcell in oldCells:

                        oldcell.add_to_y(rows_to_add)
                        oldcell.save()

                    max_row_id = int(row_id) + rows_to_add + 1
                    new_row_id = int(row_id) + 1

                    for row in range(new_row_id, max_row_id):

                        for i, column in enumerate(columns):

                            cell = Cell.create(matrix, "", "", "", i, row, "", None)
                            cell.save()

                    matrix.save()

                    imageCells = Cell.objects.filter(matrix=matrix_id)\
                                             .filter(xcoordinate=column_id)\
                                             .filter(ycoordinate__gt=0)\
                                             .filter(ycoordinate__lte=collection_image_count)\
                                             .order_by('ycoordinate')

                    imageCounter = 1

                    for imageCell in imageCells:

                        collectionimageorders = CollectionImageOrder.objects.filter(collection=collection)\
                                                                            .filter(ordering=imageCounter)\
                                                                            .filter(permitted=request.user)

                        image = None

                        for collectionimageorder in collectionimageorders:

                            image = collectionimageorder.image

                        post_id = ''

                        imageCell.title = image.name
                        imageCell.description = image.name

                        if imageCell.has_no_blogpost():

                            if credential.has_apppwd() and environment.is_wordpress_active():

                                returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                         imageCell.title,
                                                                                         imageCell.description)

                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                    post_id = returned_blogpost['id']

                            imageCell.set_blogpost(post_id)

                        imageCell.image = image

                        if request.user.profile.is_hide_collection_image():

                            image.set_hidden(True)
                            image.save()

                        imageCell.save()

                        imageCounter = imageCounter + 1

                    actual_column = int(column_id)

                    matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                    messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' + str() +
                                     ' Collection Added to Column ' + str(actual_column) + '!')

                else:

                    # the collection will fit in the available cells
                    imageCells = Cell.objects.filter(matrix=matrix_id)\
                                             .filter(xcoordinate=column_id)\
                                             .filter(ycoordinate__gt=0)\
                                             .filter(ycoordinate__lte=collection_image_count)\
                                             .order_by('ycoordinate')

                    imageCounter = 1

                    for imageCell in imageCells:

                        collectionimageorders = CollectionImageOrder.objects.filter(collection=collection)\
                                                                            .filter(ordering=imageCounter)\
                                                                            .filter(permitted=request.user)

                        image = None

                        for collectionimageorder in collectionimageorders:

                            image = collectionimageorder.image

                        post_id = ''

                        imageCell.title = image.name
                        imageCell.description = image.name

                        if imageCell.has_no_blogpost():

                            if credential.has_apppwd() and environment.is_wordpress_active():

                                returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                         imageCell.title,
                                                                                         imageCell.description)

                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                    post_id = returned_blogpost['id']

                            imageCell.set_blogpost(post_id)

                        imageCell.image = image

                        if request.user.profile.is_hide_collection_image():

                            image.set_hidden(True)
                            image.save()

                        imageCell.save()

                        imageCounter = imageCounter + 1

                    actual_column = int(column_id)

                    matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                    messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' + str() +
                                     ' Collection Added to Column ' + str(actual_column) + '!')

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells})

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
