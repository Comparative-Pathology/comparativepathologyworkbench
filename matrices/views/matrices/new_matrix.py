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
# This file contains the new_matrix view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import NewMatrixForm

from matrices.models import Cell

from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data

HTTP_POST = 'POST'
NO_CREDENTIALS = ''
WORDPRESS_SUCCESS = 'Success!'

MAX_INITIAL_COLUMNS = 51
MAX_INITIAL_ROWS = 51

#
# CREATE A NEW BENCH
#
@login_required
def new_matrix(request):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        if request.method == HTTP_POST:

            form = NewMatrixForm(request.POST)

            if form.is_valid():

                matrix = form.save(commit=False)

                rows = form.cleaned_data['rows']
                columns = form.cleaned_data['columns']

                rows = rows + 1
                columns = columns + 1

                if rows == 1:
                    rows = 2

                if columns == 1:
                    columns = 2

                if rows > MAX_INITIAL_ROWS:
                    rows = 2

                if columns > MAX_INITIAL_COLUMNS:
                    columns = 2

                if matrix.is_not_high_enough() == True:
                    matrix.set_minimum_height()

                if matrix.is_not_wide_enough() == True:
                    matrix.set_minimum_width()

                if matrix.is_too_high() == True:
                    matrix.set_maximum_height()

                if matrix.is_too_wide() == True:
                    matrix.set_maximum_width()

                credential = get_credential_for_user(request.user)

                post_id = ''

                if credential.has_apppwd():

                    returned_blogpost = serverWordpress.post_wordpress_post(credential, matrix.title, matrix.description)

                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                        post_id = returned_blogpost['id']

                    else:

                        messages.error(request, "CPW_WEB:0370 New Bench  - WordPress Error, Contact System Administrator!")
                        form.add_error(None, "CPW_WEB:0370 New Bench  - WordPress Error, Contact System Administrator!")

                        data.update({ 'form': form })

                        return render(request, 'matrices/new_matrix.html', data)


                matrix.set_blogpost(post_id)

                matrix.set_owner(request.user)

                matrix.save()

                x = 0

                while x <= columns:

                    y = 0

                    while y <= rows:

                        cell = Cell.create(matrix, "", "", x, y, "", None)

                        cell.save()

                        y = y + 1

                    x = x + 1

                matrix_id_formatted = "CPW:" + "{:06d}".format(matrix.id)
                messages.success(request, 'NEW Bench ' + matrix_id_formatted + ' Created!')

                return HttpResponseRedirect(reverse('matrix', args=(matrix.id,)))

            else:

                messages.error(request, "CPW_WEB:0380 New Bench  - Form is Invalid!")
                form.add_error(None, "CPW_WEB:0380 New Bench  - Form is Invalid!")

                data.update({ 'form': form })

        else:

            form = NewMatrixForm()

            data.update({ 'form': form })

        return render(request, 'matrices/new_matrix.html', data)
