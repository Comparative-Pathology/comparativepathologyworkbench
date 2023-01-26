#!/usr/bin/python3
###!
# \file         view_matrix_blog.py
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
# This file contains the view_matrix_blog view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import CommentForm

from matrices.models import Matrix

from matrices.routines import credential_exists
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_credential_for_user
from matrices.routines import get_header_data
from matrices.routines import get_primary_wordpress_server

HTTP_POST = 'POST'
WORDPRESS_SUCCESS = 'Success!'


#
# VIEW THE AGGREGATED BLOG ENTRies
#
@login_required
def view_aggregated_blog(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if credential_exists(request.user):

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        matrix_cells = matrix.get_matrix_cells_with_blog()

        bench_comment_list = list()

        bench_blogpost = ''

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() == True or authority.is_editor() == True or authority.is_owner() == True or authority.is_admin() == True:

            if matrix.has_blogpost():

                bench_blogpost = serverWordpress.get_wordpress_post(matrix.blogpost)

            bench_comment_list = serverWordpress.get_wordpress_post_comments(matrix.blogpost)


        data.update({ 'matrix': matrix, 'bench_blogpost': bench_blogpost, 'bench_comment_list': bench_comment_list, 'matrix_cells': matrix_cells })

        return render(request, 'matrices/aggregated_matrix_blog.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
