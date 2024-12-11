#!/usr/bin/python3
#
# ##
# \file         add_collection_column_cell_task.py
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
# The add_collection_column_cell_task Task.
# ##
#
from __future__ import absolute_import

from celery import shared_task

from django.contrib.auth.models import User

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Collection
from matrices.models import CollectionImageOrder
from matrices.models import Credential

from matrices.routines.simulate_network_latency import simulate_network_latency
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

WORDPRESS_SUCCESS = 'Success!'


#
#   Add ALL the images from a Collection to a Column from a specific Cell
#
@shared_task
def add_collection_column_cell_task(user_id, matrix_id,  cell_id):

    simulate_network_latency()

    environment = get_primary_cpw_environment()

    result_message = ''

    user = User.objects.get(id=user_id)
    matrix = Matrix.objects.get(id=matrix_id)
    cell = Cell.objects.get(id=cell_id)

    cell_xcoordinate = cell.xcoordinate
    cell_ycoordinate = cell.ycoordinate

    credential = Credential.objects.get_or_none(username=user.username)

    collection = Collection.objects.get(id=matrix.last_used_collection.id)

    collection_image_count = collection.get_images_count()

    cells = Cell.objects.filter(matrix=matrix_id)\
                        .filter(xcoordinate=cell_xcoordinate)\
                        .filter(ycoordinate__gte=cell_ycoordinate)\
                        .order_by('ycoordinate')

    free_cell_count = 0
    max_ycoordinate = 0

    for cell in cells:

        if cell.has_image():

            break

        else:

            max_ycoordinate = cell.ycoordinate

            if not cell.is_header():

                free_cell_count = free_cell_count + 1

    # Minus 1 for the footer cell
    free_cell_count = free_cell_count - 1

    row_id = max_ycoordinate - 1

    rows_to_add = 0

    if collection_image_count > free_cell_count:

        # the collection is too big for the available cells
        rows_to_add = collection_image_count - free_cell_count

        oldCells = Cell.objects.filter(matrix=matrix_id)\
                               .filter(ycoordinate__gt=row_id)

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

        cell_ycoordinate_offset = cell_ycoordinate + collection_image_count

        imageCells = Cell.objects.filter(matrix=matrix_id)\
                                 .filter(xcoordinate=cell_xcoordinate)\
                                 .filter(ycoordinate__gte=cell_ycoordinate)\
                                 .filter(ycoordinate__lt=cell_ycoordinate_offset)\
                                 .order_by('ycoordinate')

        imageCounter = 1

        for imageCell in imageCells:

            collectionimageorders = CollectionImageOrder.objects.filter(collection=collection)\
                                                                .filter(ordering=imageCounter)\
                                                                .filter(permitted=user)

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

            if user.profile.is_hide_collection_image():

                image.set_hidden(True)
                image.save()

            imageCell.save()

            imageCounter = imageCounter + 1

        actual_column = int(cell_xcoordinate)

        result_message = 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' + \
                         ' Collection Added to Column ' + str(actual_column) + \
                         ' From Cell (X:' + str(cell_xcoordinate) + \
                         ', Y:' + str(cell_ycoordinate) + ')'

    else:

        cell_ycoordinate_offset = cell_ycoordinate + collection_image_count

        # the collection will fit in the available cells
        imageCells = Cell.objects.filter(matrix=matrix_id)\
                                 .filter(xcoordinate=cell_xcoordinate)\
                                 .filter(ycoordinate__gte=cell_ycoordinate)\
                                 .filter(ycoordinate__lt=cell_ycoordinate_offset)\
                                 .order_by('ycoordinate')

        imageCounter = 1

        for imageCell in imageCells:

            collectionimageorders = CollectionImageOrder.objects.filter(collection=collection)\
                                                                .filter(ordering=imageCounter)\
                                                                .filter(permitted=user)

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

            if user.profile.is_hide_collection_image():

                image.set_hidden(True)
                image.save()

            imageCell.save()

            imageCounter = imageCounter + 1

        actual_column = int(cell_xcoordinate)

        result_message = 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' + \
                         ' Collection Added to Column ' + str(actual_column) + \
                         ' From Cell (X:' + str(cell_xcoordinate) + \
                         ', Y:' + str(cell_ycoordinate) + ')'

    matrix.set_unlocked()
    matrix.save()

    return result_message
