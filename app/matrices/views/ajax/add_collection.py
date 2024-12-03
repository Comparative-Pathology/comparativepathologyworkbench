#!/usr/bin/python3
#
# ##
# \file         add_collection.py
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
# This file contains the AJAX add_collection view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.forms import MatrixAddCollectionForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Collection
from matrices.models import CollectionImageOrder

from matrices.routines import credential_exists
from matrices.routines import exists_update_for_bench_and_user
from matrices.routines import get_credential_for_user
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_primary_cpw_environment

from background.tasks import add_collection_row_cell_task
from background.tasks import add_collection_column_cell_task

WORDPRESS_SUCCESS = 'Success!'


#
#   Add an entire Collection to a Bench Cell
#
@login_required()
def add_collection(request, matrix_id, cell_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    matrix = get_object_or_404(Matrix, pk=matrix_id)

    if matrix.is_locked():

        raise PermissionDenied

    environment = get_primary_cpw_environment()

    if credential_exists(request.user):

        credential = get_credential_for_user(request.user)

        owner = matrix.owner

        cell = get_object_or_404(Cell, pk=cell_id)

        cell_xcoordinate = cell.xcoordinate
        cell_ycoordinate = cell.ycoordinate

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            if authority.is_editor():

                owner = request.user

            template_name = 'frontend_forms/generic_form_inner.html'

            if request.method == 'POST':

                form = MatrixAddCollectionForm(data=request.POST)

                if form.is_valid():

                    cd = form.cleaned_data

                    direction = int(cd.get('direction'))

                    # PUSH Right - Add Collection to ROW
                    if direction == 1:

                        if exists_update_for_bench_and_user(matrix, request.user):

                            if environment.is_background_processing():

                                matrix.set_locked()
                                matrix.save()

                                result = add_collection_row_cell_task.delay_on_commit(owner.id, 
                                                                                      matrix.id, 
                                                                                      cell.id)

                                matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                                messages.error(request, 'Bench ' + matrix_id_formatted + ' LOCKED pending Update!')

                            else:

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

                                        collectionimageorders = CollectionImageOrder.objects\
                                                                    .filter(collection=collection)\
                                                                    .filter(ordering=imageCounter)\
                                                                    .filter(permitted=owner)

                                        image = None

                                        for collectionimageorder in collectionimageorders:

                                            image = collectionimageorder.image

                                        post_id = ''

                                        imageCell.title = image.name
                                        imageCell.description = image.name

                                        if imageCell.has_no_blogpost():

                                            if credential.has_apppwd() and environment.is_wordpress_active():

                                                returned_blogpost = environment\
                                                                    .post_a_post_to_wordpress(credential,
                                                                                              imageCell.title,
                                                                                              imageCell.description)

                                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                                    post_id = returned_blogpost['id']

                                            imageCell.set_blogpost(post_id)

                                        imageCell.image = image

                                        if owner.profile.is_hide_collection_image():

                                            image.set_hidden(True)
                                            image.save()

                                        imageCell.save()

                                        imageCounter = imageCounter + 1

                                    actual_row = int(cell_ycoordinate)

                                    matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                                    messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' +
                                                 ' Collection Added to Row ' + str(actual_row) +
                                                 ' From Cell (X:' + str(cell_xcoordinate) +
                                                 ', Y:' + str(cell_ycoordinate) + ')')

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

                                        collectionimageorders = CollectionImageOrder.objects\
                                                                    .filter(collection=collection)\
                                                                    .filter(ordering=imageCounter)\
                                                                    .filter(permitted=owner)

                                        image = None

                                        for collectionimageorder in collectionimageorders:

                                            image = collectionimageorder.image

                                        post_id = ''

                                        imageCell.title = image.name
                                        imageCell.description = image.name

                                        if imageCell.has_no_blogpost():

                                            if credential.has_apppwd() and environment.is_wordpress_active():

                                                returned_blogpost = environment\
                                                                    .post_a_post_to_wordpress(credential,
                                                                                              imageCell.title,
                                                                                              imageCell.description)

                                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                                    post_id = returned_blogpost['id']

                                            imageCell.set_blogpost(post_id)

                                        imageCell.image = image

                                        if owner.profile.is_hide_collection_image():

                                            image.set_hidden(True)
                                            image.save()

                                        imageCell.save()

                                        imageCounter = imageCounter + 1

                                    actual_row = int(cell_ycoordinate)

                                    matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                                    messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' +
                                                     ' Collection Added to Row ' + str(actual_row) +
                                                     ' From Cell (X:' + str(cell_xcoordinate) +
                                                     ', Y:' + str(cell_ycoordinate) + ')')

                    # PUSH Down - Add Collection to COLUMN
                    else:

                        if exists_update_for_bench_and_user(matrix, request.user):

                            if environment.is_background_processing():

                                matrix.set_locked()
                                matrix.save()

                                result = add_collection_column_cell_task.delay_on_commit(owner.id,
                                                                                         matrix.id,
                                                                                         cell.id)

                                matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                                messages.error(request, 'Bench ' + matrix_id_formatted + ' LOCKED pending Update!')

                            else:

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

                                        collectionimageorders = CollectionImageOrder.objects\
                                                                    .filter(collection=collection)\
                                                                    .filter(ordering=imageCounter)\
                                                                    .filter(permitted=owner)

                                        image = None

                                        for collectionimageorder in collectionimageorders:

                                            image = collectionimageorder.image

                                        post_id = ''

                                        imageCell.title = image.name
                                        imageCell.description = image.name

                                        if imageCell.has_no_blogpost():

                                            if credential.has_apppwd() and environment.is_wordpress_active():

                                                returned_blogpost = environment\
                                                                    .post_a_post_to_wordpress(credential,
                                                                                              imageCell.title,
                                                                                              imageCell.description)

                                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                                    post_id = returned_blogpost['id']

                                            imageCell.set_blogpost(post_id)

                                        imageCell.image = image

                                        if owner.profile.is_hide_collection_image():

                                            image.set_hidden(True)
                                            image.save()

                                        imageCell.save()

                                        imageCounter = imageCounter + 1

                                    actual_column = int(cell_xcoordinate)

                                    matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                                    messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' +
                                                     ' Collection Added to Column ' + str(actual_column) +
                                                     ' From Cell (X:' + str(cell_xcoordinate) +
                                                     ', Y:' + str(cell_ycoordinate) + ')')

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

                                        collectionimageorders = CollectionImageOrder.objects\
                                                                    .filter(collection=collection)\
                                                                    .filter(ordering=imageCounter)\
                                                                    .filter(permitted=owner)

                                        image = None

                                        for collectionimageorder in collectionimageorders:

                                            image = collectionimageorder.image

                                        post_id = ''

                                        imageCell.title = image.name
                                        imageCell.description = image.name

                                        if imageCell.has_no_blogpost():

                                            if credential.has_apppwd() and environment.is_wordpress_active():

                                                returned_blogpost = environment\
                                                                        .post_a_post_to_wordpress(credential,
                                                                                                  imageCell.title,
                                                                                                  imageCell.description)

                                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                                    post_id = returned_blogpost['id']

                                            imageCell.set_blogpost(post_id)

                                        imageCell.image = image

                                        if owner.profile.is_hide_collection_image():

                                            image.set_hidden(True)
                                            image.save()

                                        imageCell.save()

                                        imageCounter = imageCounter + 1

                                    actual_column = int(cell_xcoordinate)

                                    matrix_id_formatted = "CPW:" + "{:06d}".format(matrix_id)
                                    messages.success(request, 'EXISTING Bench ' + matrix_id_formatted + ' Updated - ' +
                                                     ' Collection Added to Column ' + str(actual_column) +
                                                     ' From Cell (X:' + str(cell_xcoordinate) +
                                                     ', Y:' + str(cell_ycoordinate) + ')')

            else:

                form = MatrixAddCollectionForm()
                form.fields['direction'].initial = [1]

            return render(request, template_name, {
                'form': form,
            })

    else:

        raise PermissionDenied
