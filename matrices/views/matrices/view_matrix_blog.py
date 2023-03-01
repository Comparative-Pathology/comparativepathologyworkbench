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
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

HTTP_POST = 'POST'
WORDPRESS_SUCCESS = 'Success!'


#
# VIEW THE BENCH BLOG ENTRY
#
@login_required
def view_matrix_blog(request, matrix_id):

    environment = get_primary_cpw_environment()

    data = get_header_data(request.user)

    if credential_exists(request.user):

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        matrix_cells = matrix.get_matrix()
        columns = matrix.get_columns()
        rows = matrix.get_rows()

        blogpost = ''

        comment_list = list()

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() == True or authority.is_editor() == True or authority.is_owner() == True or authority.is_admin() == True:

            if matrix.has_blogpost():

                blogpost = environment.get_a_post_from_wordpress(matrix.blogpost)

                if blogpost['status'] != WORDPRESS_SUCCESS:

                    credential = get_credential_for_user(request.user)

                    post_id = ''

                    if credential.has_apppwd():

                        returned_blogpost = environment.post_a_post_to_wordpress(credential, matrix.title, matrix.description)

                        if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                            post_id = returned_blogpost['id']

                    matrix.set_blogpost(post_id)

                    matrix.save()

                    blogpost = environment.get_a_post_from_wordpress(matrix.blogpost)

            else:

                credential = get_credential_for_user(request.user)

                post_id = ''

                if credential.has_apppwd():

                    returned_blogpost = environment.post_a_post_to_wordpress(credential, matrix.title, matrix.description)

                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                        post_id = returned_blogpost['id']

                matrix.set_blogpost(post_id)

                matrix.save()

                blogpost = environment.get_a_post_from_wordpress(matrix.blogpost)


            comment_list = environment.get_a_post_comments_from_wordpress(matrix.blogpost)

        if request.method == HTTP_POST:

            form = CommentForm(request.POST)

            if form.is_valid():

                cd = form.cleaned_data

                comment = cd.get('comment')

                if comment != '':

                    credential = get_credential_for_user(request.user)

                    returned_comment = environment.post_a_comment_to_wordpress(credential, matrix.blogpost, comment)

                return HttpResponseRedirect(reverse('detail_matrix_blog', args=(matrix_id,)))

            else:

                messages.error(request, "CPW_WEB:0580 View Bench Blog - Form is Invalid!")

        else:

            form = CommentForm()

        data.update({ 'form': form, 'matrix': matrix, 'blogpost': blogpost, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'comment_list': comment_list })

        return render(request, 'matrices/detail_matrix_blog.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
