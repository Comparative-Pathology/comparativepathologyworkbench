#!/usr/bin/python3
###!
# \file		 views_matrices.py
# \author	   Mike Wicks
# \date		 March 2021
# \version	  $Id$
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
# This file contains the amend_cell view routine
#
###
from __future__ import unicode_literals

import subprocess
from subprocess import call

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from decouple import config

from matrices.forms import SearchUrlForm

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import add_image_to_collection
from matrices.routines import convert_url_ebi_sca_to_json
from matrices.routines import convert_url_omero_image_to_cpw
from matrices.routines import convert_url_ebi_sca_to_chart_id
from matrices.routines import create_an_ebi_sca_chart
from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_active_collection_images_for_user
from matrices.routines import get_an_ebi_sca_experiment_id
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_blog_link_post_url
from matrices.routines import get_credential_for_user
from matrices.routines import get_header_data
from matrices.routines.get_id_from_omero_url import get_id_from_omero_url
from matrices.routines import get_images_for_collection
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_server_from_ebi_sca_url
from matrices.routines import get_server_from_omero_url

HTTP_POST = 'POST'
WORDPRESS_SUCCESS = 'Success!'

#
# VIEW THE CELL DETAILS
#
@login_required
def amend_cell(request, matrix_id, cell_id):

    if request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied


    if credential_exists(request.user):

        data = get_header_data(request.user)
        serverWordpress = get_primary_wordpress_server()

        cell = get_object_or_404(Cell, pk=cell_id)
        matrix = get_object_or_404(Matrix, pk=matrix_id)

        if exists_read_for_bench_and_user(matrix, request.user):

            cell_link = get_blog_link_post_url() + cell.blogpost

            matrix_link = 'matrix_link'
            amend_cell = 'amend_cell'

            credential = get_credential_for_user(request.user)

            if not credential.has_apppwd():

                matrix_link = ''

            collection_image_list = list()

            if matrix.has_last_used_collection():

                collection_image_list = get_images_for_collection(matrix.last_used_collection)

            else:

                if exists_active_collection_for_user(request.user):

                    collection_image_list = get_active_collection_images_for_user(request.user)
                    collection_list = get_active_collection_for_user(request.user)
                    collection = collection_list[0]

                    matrix.set_last_used_collection(collection)
                    matrix.save()

            if request.method == HTTP_POST:

                form = SearchUrlForm(request.POST)

                image = None

                if form.is_valid():

                    cd = form.cleaned_data

                    url_string = cd.get('url_string')

                    url_string_ebi_sca_out = convert_url_ebi_sca_to_json(url_string)
                    url_string_omero_out = convert_url_omero_image_to_cpw(request, url_string)

                    if url_string_omero_out != '' and url_string_ebi_sca_out != '':

                        messages.error(request, "CPW_WEB:0210 Amend Cell - URL not found!")
                        form.add_error(None, "CPW_WEB:0210 Amend Cell - URL not found!")

                        data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                        return render(request, 'matrices/amend_cell.html', data)


                    if url_string_omero_out == '' and url_string_ebi_sca_out == '':

                        messages.error(request, "CPW_WEB:0220 Amend Cell - URL not found!")
                        form.add_error(None, "CPW_WEB:0220 Amend Cell - URL not found!")

                        data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                        return render(request, 'matrices/amend_cell.html', data)


                    if url_string_omero_out != '' and url_string_ebi_sca_out == '':

                        server = get_server_from_omero_url(url_string_omero_out)
                        image_id = get_id_from_omero_url(url_string_omero_out)

                        if exists_active_collection_for_user(request.user):

                            image = add_image_to_collection(request.user, server, image_id, 0)

                            queryset = get_active_collection_for_user(request.user)

                            for collection in queryset:

                                matrix.set_last_used_collection(collection)

                        else:

                            messages.error(request, "CPW_WEB:0230 Amend Cell - You have no Active Image Collection; Please create a Collection!")
                            form.add_error(None, "CPW_WEB:0230 Amend Cell - You have no Active Image Collection; Please create a Collection!")

                            data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                            return render(request, 'matrices/amend_cell.html', data)


                    if url_string_omero_out == '' and url_string_ebi_sca_out != '':

                        temp_dir = config('HIGHCHARTS_TEMP_DIR')
                        output_dir = config('HIGHCHARTS_OUTPUT_DIR')
                        highcharts_host = config('HIGHCHARTS_HOST')
                        highcharts_web = config('HIGHCHARTS_OUTPUT_WEB')

                        experiment_id = get_an_ebi_sca_experiment_id(url_string)

                        image_id = convert_url_ebi_sca_to_chart_id(url_string)

                        shell_command = create_an_ebi_sca_chart(url_string_ebi_sca_out, experiment_id, image_id, highcharts_host, temp_dir, output_dir)

                        success = call(str(shell_command), shell=True)

                        if success == 0:

                            server = get_server_from_ebi_sca_url(url_string_ebi_sca_out)

                            if exists_active_collection_for_user(request.user):

                                image = add_image_to_collection(request.user, server, image_id, 0)

                                queryset = get_active_collection_for_user(request.user)

                                for collection in queryset:

                                    matrix.set_last_used_collection(collection)

                            else:

                                messages.error(request, "CPW_WEB:0240 Amend Cell - You have no Active Image Collection; Please create a Collection!")
                                form.add_error(None, "CPW_WEB:0240 Amend Cell - You have no Active Image Collection; Please create a Collection!")

                                data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                                return render(request, 'matrices/amend_cell.html', data)

                        else:

                            messages.error(request, "CPW_WEB:0250 Amend Cell - Unable to generate Chart, shell_command FAILED!")
                            form.add_error(None, "CPW_WEB:0250 Amend Cell - Unable to generate Chart, shell_command FAILED!")

                            data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                            return render(request, 'matrices/amend_cell.html', data)


                    cell.set_title(image.name)
                    cell.set_description(image.name)
                    cell.set_image(image)
                    cell.set_matrix(matrix)

                    post_id = ''

                    if cell.has_no_blogpost():

                        credential = get_credential_for_user(request.user)

                        if credential.has_apppwd():

                            returned_blogpost = serverWordpress.post_wordpress_post(credential, cell.title, cell.description)

                            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                post_id = returned_blogpost['id']
                                cell.set_blogpost(post_id)

                            else:

                                messages.error(request, "CPW_WEB:0260 Amend Cell - WordPress Error, Contact System Administrator!")
                                form.add_error(None, "CPW_WEB:0260 Amend Cell - WordPress Error, Contact System Administrator!")

                                data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                                return render(request, 'matrices/amend_cell.html', data)

                    cell.save()

                    matrix.save()

                    cell_id_formatted = "CPW:" + "{:06d}".format(matrix.id) + "_" + str(cell.id)

                    messages.success(request, 'Cell ' + cell_id_formatted + ' Updated!')

                else:

                    messages.error(request, "CPW_WEB:0270 Amend Cell - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0270 Amend Cell - Form is Invalid!")

                    data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

                    return render(request, 'matrices/amend_cell.html', data)

            form = SearchUrlForm()

            data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

            return render(request, 'matrices/amend_cell.html', data)

        else:

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

    else:

        raise PermissionDenied
