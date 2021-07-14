#!/usr/bin/python3
###!
# \file         views_matrices.py
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
# This file contains the edit_cell view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from urllib.parse import urlparse

from matrices.forms import SearchUrlForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Server

from matrices.routines import add_image_to_collection
from matrices.routines import convert_url_omero_image_to_cpw
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_credential_for_user
from matrices.routines import get_header_data
from matrices.routines import get_primary_wordpress_server

HTTP_POST = 'POST'
NO_CREDENTIALS = ''
WORDPRESS_SUCCESS = 'Success!'

#
# UPDATE THE CELL BY ADDING AN IMAGE FROM A URL
#
@login_required
def update_cell(request, matrix_id, cell_id):

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

			if request.method == HTTP_POST:

				form = SearchUrlForm(request.POST)

				image = None

				if form.is_valid():

					cd = form.cleaned_data

					url_string = cd.get('url_string')

					url_string_out = convert_url_omero_image_to_cpw(request, url_string)

					if url_string_out == "":

						messages.error(request, "URL not found!")
						form.add_error(None, "URL not found!")

						data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

						return render(request, 'matrices/update_cell.html', data)

					else:

						u = urlparse(url_string_out)

						query_path = u.path

						query_array = query_path.split("/")

						query_server = query_array[2]
						query_id = query_array[3]

						server = get_object_or_404(Server, pk=query_server)

						if exists_active_collection_for_user(request.user):

							image = add_image_to_collection(request.user, server, query_id, 0)

							queryset = get_active_collection_for_user(request.user)

							for collection in queryset:

								matrix.set_last_used_collection(collection)

						else:

							messages.error(request, "ERROR: You have no Active Image Collection; Please create a Collection!")
							form.add_error(None, "ERROR: You have no Active Image Collection; Please create a Collection!")

							data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

							return render(request, 'matrices/update_cell.html', data)


						cell.set_title(image.name)
						cell.set_description(image.name)

						cell.set_image(image)

						cell.set_matrix(matrix)

						post_id = ''

						if cell.has_no_blogpost() == True:

							credential = get_credential_for_user(request.user)

							if credential.has_apppwd():

								returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, cell.title, cell.description)

								if returned_blogpost['status'] == WORDPRESS_SUCCESS:

									post_id = returned_blogpost['id']

								else:

									messages.error(request, "ERROR: WordPress Error - Contact System Administrator!")
									form.add_error(None, "ERROR: WordPress Error - Contact System Administrator!")

									data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

									return render(request, 'matrices/update_cell.html', data)


						cell.set_blogpost(post_id)

						cell.save()

						matrix.save()

				else:

					messages.error(request, "ERROR: Form is Invalid!")
					form.add_error(None, "ERROR: Form is Invalid!")

					data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

					return render(request, 'matrices/update_cell.html', data)


				matrix_cells = matrix.get_matrix()
				columns = matrix.get_columns()
				rows = matrix.get_rows()

				data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

				return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

			else:

				form = SearchUrlForm()

			data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

			return render(request, 'matrices/update_cell.html', data)
