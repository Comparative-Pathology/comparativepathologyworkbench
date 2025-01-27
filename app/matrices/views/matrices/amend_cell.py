#!/usr/bin/python3
# 
# ##
# \file		   amend_cell.py
# \author	   Mike Wicks
# \date		   March 2021
# \version	   $Id$
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
# This file contains the amend_cell view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import SearchUrlForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import add_image_to_collection
from matrices.routines import convert_url_omero_image_to_cpw
from matrices.routines import exists_read_for_bench_and_user
from matrices.routines import get_header_data
from matrices.routines.get_id_from_omero_url import get_id_from_omero_url
from matrices.routines import get_server_from_omero_url
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines import is_request_ajax

HTTP_POST = 'POST'
WORDPRESS_SUCCESS = 'Success!'


#
#   VIEW THE CELL DETAILS
#
@login_required
def amend_cell(request, matrix_id, cell_id):

    if is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    cell = Cell.objects.get_or_none(id=cell_id)

    if not cell:

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=matrix_id)

    if not matrix:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        data = get_header_data(request.user)
        environment = get_primary_cpw_environment()

        if exists_read_for_bench_and_user(matrix, request.user):

            cell_link = environment.get_a_link_url_to_post() + cell.blogpost

            matrix_link = 'matrix_link'
            amend_cell = 'amend_cell'

            if not credential.has_apppwd() and environment.is_wordpress_active():

                matrix_link = ''

            collection_image_list = list()

            if matrix.has_last_used_collection():

                collection_image_list = matrix.last_used_collection.get_images()

            if request.method == HTTP_POST:

                form = SearchUrlForm(request.POST)

                image = None

                if form.is_valid():

                    cd = form.cleaned_data

                    url_string = cd.get('url_string')

                    url_string_omero_out = convert_url_omero_image_to_cpw(request, url_string)

                    if url_string_omero_out == '':

                        messages.error(request, "CPW_WEB:0220 Amend Cell - URL not found!")
                        form.add_error(None, "CPW_WEB:0220 Amend Cell - URL not found!")

                        data.update({'form': form,
                                     'collection_image_list': collection_image_list,
                                     'amend_cell': amend_cell,
                                     'matrix_link': matrix_link,
                                     'cell': cell,
                                     'cell_link': cell_link,
                                     'matrix': matrix})

                        return render(request, 'matrices/amend_cell.html', data)

                    else:

                        server = get_server_from_omero_url(url_string_omero_out)

                        if server:

                            image_id = get_id_from_omero_url(url_string_omero_out)

                            if request.user.profile.has_active_collection():

                                collection = request.user.profile.active_collection

                                image = add_image_to_collection(request.user, server, image_id, 0, collection.id)

                                matrix.set_last_used_collection(collection)

                            else:

                                messages.error(request, "CPW_WEB:0230 Amend Cell - You have no Active Image Collection; " +
                                               "Please create a Collection!")
                                form.add_error(None, "CPW_WEB:0230 Amend Cell - You have no Active Image Collection; " +
                                               "Please create a Collection!")

                                data.update({'form': form,
                                             'collection_image_list': collection_image_list,
                                             'amend_cell': amend_cell,
                                             'matrix_link': matrix_link,
                                             'cell': cell,
                                             'cell_link': cell_link,
                                             'matrix': matrix})

                                return render(request, 'matrices/amend_cell.html', data)

                        else:

                            raise PermissionDenied

                    cell.set_title(image.name)
                    cell.set_description(image.name)
                    cell.set_image(image)
                    cell.set_matrix(matrix)

                    post_id = ''

                    if cell.has_no_blogpost():

                        if credential.has_apppwd() and environment.is_wordpress_active():

                            returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                     cell.title,
                                                                                     cell.description)

                            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                post_id = returned_blogpost['id']
                                cell.set_blogpost(post_id)

                            else:

                                messages.error(request, "CPW_WEB:0260 Amend Cell - WordPress Error, Contact System " +
                                               "Administrator!")
                                form.add_error(None, "CPW_WEB:0260 Amend Cell - WordPress Error, Contact System " +
                                               "Administrator!")

                                data.update({'form': form,
                                             'collection_image_list': collection_image_list,
                                             'amend_cell': amend_cell,
                                             'matrix_link': matrix_link,
                                             'cell': cell,
                                             'cell_link': cell_link,
                                             'matrix': matrix})

                                return render(request, 'matrices/amend_cell.html', data)

                    cell.save()

                    matrix.save()

                    messages.success(request, 'Cell ' + cell.get_formatted_id() + ' Updated!')

                    data.update({'form': form,
                                 'collection_image_list': collection_image_list,
                                 'amend_cell': amend_cell,
                                 'matrix_link': matrix_link,
                                 'cell': cell,
                                 'cell_link': cell_link,
                                 'matrix': matrix})

                    return HttpResponseRedirect(reverse('amend_cell', args=(matrix_id, cell_id, )))

                else:

                    messages.error(request, "CPW_WEB:0270 Amend Cell - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0270 Amend Cell - Form is Invalid!")

                    data.update({'form': form,
                                 'collection_image_list': collection_image_list,
                                 'amend_cell': amend_cell,
                                 'matrix_link': matrix_link,
                                 'cell': cell,
                                 'cell_link': cell_link,
                                 'matrix': matrix})

                    return render(request, 'matrices/amend_cell.html', data)

            form = SearchUrlForm()

            data.update({'form': form,
                         'collection_image_list': collection_image_list,
                         'amend_cell': amend_cell,
                         'matrix_link': matrix_link,
                         'cell': cell,
                         'cell_link': cell_link,
                         'matrix': matrix})

            return render(request, 'matrices/amend_cell.html', data)

        else:

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells})

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

    else:

        raise PermissionDenied
