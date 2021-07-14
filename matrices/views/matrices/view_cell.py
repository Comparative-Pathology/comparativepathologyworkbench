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
# This file contains the view_cell view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import get_blog_link_post_url
from matrices.routines import get_header_data

NO_CREDENTIALS = ''

#
# VIEW THE CELL DETAILS
#
@login_required
def view_cell(request, matrix_id, cell_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        cell = get_object_or_404(Cell, pk=cell_id)

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        cell_link = get_blog_link_post_url() + cell.blogpost

        data.update({'cell': cell, 'cell_link': cell_link, 'matrix': matrix })

        return render(request, 'matrices/detail_cell.html', data)
