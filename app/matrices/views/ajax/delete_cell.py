#!/usr/bin/python3
#
# ##
# \file         delete_cell.py
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
# This file contains the AJAX delete_cell view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import MatrixDeleteCellForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import exists_collections_for_image
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_cells_for_image
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines import is_request_ajax

WORDPRESS_SUCCESS = 'Success!'


#
#   Delete a Cell
#
@login_required()
def delete_cell(request, matrix_id, cell_id):

    environment = get_primary_cpw_environment()

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=matrix_id)

    if not matrix:

        raise PermissionDenied

    if matrix.is_locked():

        raise PermissionDenied

    cell = Cell.objects.get_or_none(id=cell_id)

    if not cell:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            template_name = 'frontend_forms/generic_form_inner.html'

            if request.method == 'POST':

                form = MatrixDeleteCellForm(data=request.POST)

                if form.is_valid():

                    cd = form.cleaned_data

                    direction = int(cd.get('direction'))

                    # PULL Left
                    if direction == 1:

                        shuffleCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate__gte=cell.xcoordinate)\
                                                   .filter(ycoordinate=cell.ycoordinate)

                        for shuffleCell in shuffleCells:

                            shuffleCell.decrement_x()

                            if shuffleCell.xcoordinate < cell.xcoordinate:

                                shuffleCell.xcoordinate = matrix.get_max_column()

                                if shuffleCell.has_blogpost():

                                    if credential.has_apppwd() and environment.is_wordpress_active():

                                        response = environment.delete_a_post_from_wordpress(credential,
                                                                                            shuffleCell.blogpost)

                                        if response != WORDPRESS_SUCCESS:

                                            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

                                if shuffleCell.has_image():

                                    if exists_collections_for_image(shuffleCell.image):

                                        cell_list = get_cells_for_image(shuffleCell.image)

                                        other_bench_Flag = False

                                        for otherCell in cell_list:

                                            if otherCell.matrix.id != matrix.id:

                                                other_bench_Flag = True

                                        if other_bench_Flag:

                                            if request.user.profile.is_hide_collection_image():

                                                shuffleCell.image.set_hidden(True)
                                                shuffleCell.image.save()

                                            else:

                                                shuffleCell.image.set_hidden(False)
                                                shuffleCell.image.save()

                                        else:

                                            shuffleCell.image.set_hidden(False)
                                            shuffleCell.image.save()

                                    else:

                                        cell_list = get_cells_for_image(shuffleCell.image)

                                        delete_flag = True

                                        for otherCell in cell_list:

                                            if otherCell.matrix.id != matrix_id:

                                                delete_flag = False

                                        if delete_flag:

                                            image = shuffleCell.image

                                            image.delete()

                                    shuffleCell.set_blogpost('')
                                    shuffleCell.set_title('')
                                    shuffleCell.set_description('')

                                    shuffleCell.image = None

                            shuffleCell.save()

                        messages.success(request, 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' + str()
                                         + ' Cell Deleted with Pull Left!')

                    # PULL Up
                    else:

                        shuffleCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate=cell.xcoordinate)\
                                                   .filter(ycoordinate__gte=cell.ycoordinate)

                        for shuffleCell in shuffleCells:

                            shuffleCell.decrement_y()

                            if shuffleCell.ycoordinate < cell.ycoordinate:

                                shuffleCell.ycoordinate = matrix.get_max_row()

                                if shuffleCell.has_blogpost():

                                    if credential.has_apppwd() and environment.is_wordpress_active():

                                        response = environment.delete_a_post_from_wordpress(credential,
                                                                                            shuffleCell.blogpost)

                                        if response != WORDPRESS_SUCCESS:

                                            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

                                if shuffleCell.has_image():

                                    if exists_collections_for_image(shuffleCell.image):

                                        cell_list = get_cells_for_image(shuffleCell.image)

                                        other_bench_Flag = False

                                        for otherCell in cell_list:

                                            if otherCell.matrix.id != matrix.id:

                                                other_bench_Flag = True

                                        if other_bench_Flag:

                                            if request.user.profile.is_hide_collection_image():

                                                shuffleCell.image.set_hidden(True)
                                                shuffleCell.image.save()

                                            else:

                                                shuffleCell.image.set_hidden(False)
                                                shuffleCell.image.save()

                                        else:

                                            shuffleCell.image.set_hidden(False)
                                            shuffleCell.image.save()

                                    else:

                                        cell_list = get_cells_for_image(shuffleCell.image)

                                        delete_flag = True

                                        for otherCell in cell_list:

                                            if otherCell.matrix.id != matrix_id:

                                                delete_flag = False

                                        if delete_flag:

                                            image = shuffleCell.image

                                            image.delete()

                                    shuffleCell.set_blogpost('')
                                    shuffleCell.set_title('')
                                    shuffleCell.set_description('')

                                    shuffleCell.image = None

                            shuffleCell.save()

                        messages.success(request, 'EXISTING Bench ' + matrix.get_formatted_id() + ' Updated - ' + str()
                                         + ' Cell Deleted with Pull Up!')

            else:

                form = MatrixDeleteCellForm()
                form.fields['direction'].initial = [1]

            return render(request, template_name, {'form': form, })

    else:

        raise PermissionDenied
