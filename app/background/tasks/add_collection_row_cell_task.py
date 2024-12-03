#!/usr/bin/python3
#
# ##
# \file         add_collection_row_cell_task.py
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
# The add_collection_row_cell_task Task.
# ##
#
from __future__ import absolute_import

from celery import shared_task

from django.contrib.auth.models import User

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Collection
from matrices.models import CollectionImageOrder

from matrices.routines import get_credential_for_user
from matrices.routines.simulate_network_latency import simulate_network_latency
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

WORDPRESS_SUCCESS = 'Success!'


#
#   Add ALL the images from a Collection to a Row from a specific Cell
#
@shared_task
def add_collection_row_cell_task(user_id, matrix_id, cell_id):

    simulate_network_latency()

    result_message = ''

    user = User.objects.get(id=user_id)
    matrix = Matrix.objects.get(id=matrix_id)
    cell = Cell.objects.get(id=cell_id)

    cell_xcoordinate = cell.xcoordinate
    cell_ycoordinate = cell.ycoordinate

    environment = get_primary_cpw_environment()
    credential = get_credential_for_user(user)

    collection = Collection.objects.get(id=matrix.last_used_collection.id)

    collection_image_count = collection.get_images_count()

    cells = Cell.objects.filter(matrix=matrix_id)\
                        .filter(ycoordinate=cell_ycoordinate)\
                        .filter(xcoordinate__gte=cell_xcoordinate)\
                        .order_by('xcoordinate')

    free_cell_count = 0
    max_xcoordinate = 0

    for cell in cells:

        if cell.has_image():

            break

        else:

            max_xcoordinate = cell.xcoordinate

            if not cell.is_header():

                free_cell_count = free_cell_count + 1

    # Deduct 1 for the Footer cell only
    free_cell_count = free_cell_count - 1

    column_id = max_xcoordinate - 1

    columns_to_add = 0

    if collection_image_count > free_cell_count:

        # the collection is too big for the available cells
        columns_to_add = collection_image_count - free_cell_count

        oldCells = Cell.objects.filter(matrix=matrix_id)\
                               .filter(xcoordinate__gt=column_id)

        rows = matrix.get_rows()

        for oldcell in oldCells:

            oldcell.add_to_x(columns_to_add)
            oldcell.save()

        max_column_id = int(column_id) + columns_to_add + 1
        new_column_id = int(column_id) + 1

        for column in range(new_column_id, max_column_id):

            for i, row in enumerate(rows):

                cell = Cell.create(matrix, "", "", "", column, i, "", None)
                cell.save()

        matrix.save()

        cell_xcoordinate_offset = cell_xcoordinate + collection_image_count

        imageCells = Cell.objects.filter(matrix=matrix_id)\
                                 .filter(ycoordinate=cell_ycoordinate)\
                                 .filter(xcoordinate__gte=cell_xcoordinate)\
                                 .filter(xcoordinate__lt=cell_xcoordinate_offset)\
                                 .order_by('xcoordinate')

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

        actual_row = int(cell_ycoordinate)

        matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
        result_message = 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' + str() + \
                         ' Collection Added to Row ' + str(actual_row) + \
                         ' From Cell (X:' + str(cell_xcoordinate) + \
                         ', Y:' + str(cell_ycoordinate) + ')'

    else:

        # the collection will fit in the available cells
        cell_xcoordinate_offset = cell_xcoordinate + collection_image_count

        imageCells = Cell.objects.filter(matrix=matrix_id)\
                                 .filter(ycoordinate=cell_ycoordinate)\
                                 .filter(xcoordinate__gte=cell_xcoordinate)\
                                 .filter(xcoordinate__lt=cell_xcoordinate_offset)\
                                 .order_by('xcoordinate')

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

        actual_row = int(cell_ycoordinate)

        matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
        result_message = 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' + str() + \
                         ' Collection Added to Row ' + str(actual_row) + \
                         ' From Cell (X:' + str(cell_xcoordinate) + \
                         ', Y:' + str(cell_ycoordinate) + ')'

    matrix.set_unlocked()
    matrix.save()

    return result_message
