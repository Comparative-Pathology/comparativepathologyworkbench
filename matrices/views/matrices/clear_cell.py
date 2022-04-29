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
# This file contains the clear_cell view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import SearchUrlForm

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import exists_collections_for_image
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_blog_link_post_url
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user
from matrices.routines import get_images_for_collection
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data

VIEW_MATRIX = "view_matrix"
AMEND_CELL = "amend_cell"

WORDPRESS_SUCCESS = 'Success!'
NO_CREDENTIALS = ''

#
# CLEAR THE CELL
#
@login_required
def clear_cell(request, matrix_id, cell_id, path_from):

	serverWordpress = get_primary_wordpress_server()

	data = get_header_data(request.user)

	if data["credential_flag"] == NO_CREDENTIALS:

		return HttpResponseRedirect(reverse('home', args=()))

	else:

		cell = get_object_or_404(Cell, pk=cell_id)
		matrix = get_object_or_404(Matrix, pk=matrix_id)

		authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

		if authority.is_viewer() == True or authority.is_none() == True:

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

			return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

		else:

			if cell.has_blogpost() == True:

				credential = get_credential_for_user(request.user)

				if credential.has_apppwd():

					response = serverWordpress.delete_wordpress_post(credential, cell.blogpost)

					if response != WORDPRESS_SUCCESS:

						matrix_cells = matrix.get_matrix()
						columns = matrix.get_columns()
						rows = matrix.get_rows()

						data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

						return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


			if cell.has_image():

				if not exists_collections_for_image(cell.image):

					cell_list = get_cells_for_image(cell.image)

					delete_flag = True

					for otherCell in cell_list:

						if otherCell.matrix.id != matrix_id:

							delete_flag = False

					if delete_flag == True:

						image = cell.image

						image.delete()

				cell.set_blogpost('')
				cell.set_title('')
				cell.set_description('')

				cell.image = None

				cell.save()

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			cell_id_formatted = "CPW:" + "{:06d}".format(matrix.id) + "_" + str(cell.id)

			messages.success(request, 'Cell ' + cell_id_formatted + ' Updated!')

			if path_from == AMEND_CELL:

				collection_image_list = get_images_for_collection(matrix.last_used_collection)

				form = SearchUrlForm()

				cell_link = get_blog_link_post_url() + cell.blogpost

				matrix_link = 'matrix_link'
				amend_cell = 'amend_cell'

				credential = get_credential_for_user(request.user)

				if not credential.has_apppwd():

					matrix_link = ''

				return_page = 'matrices/amend_cell.html'

				data.update({ 'form': form, 'collection_image_list': collection_image_list, 'amend_cell': amend_cell, 'matrix_link': matrix_link, 'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

				return HttpResponseRedirect(reverse('amend_cell', args=(matrix_id, cell_id, )))
				#return render(request, return_page, data)

			else:

				if path_from == VIEW_MATRIX:

					data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

					return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

			data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

			return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))
