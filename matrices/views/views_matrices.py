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
# This contains the delete_image, detail_collection, view_collection,
# view_active_collection, new_collection, edit_collection, delete_collection,
# choose_collection, activate_collection, view_matrix_blog, view_cell_blog,
# view_matrix, new_matrix, edit_matrix, delete_matrix, add_cell, edit_cell,
# view_cell, append_column, add_column_left, add_column_right,
# delete_this_column, delete_last_column, append_row, add_row_above,
# add_row_below, delete_this_row and delete_last_row views
###
from __future__ import unicode_literals

import os
import time
import requests

from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string

from decouple import config

from matrices.forms import MatrixForm
from matrices.forms import NewMatrixForm
from matrices.forms import CellForm
from matrices.forms import HeaderForm
from matrices.forms import CommentForm
from matrices.forms import CollectionForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Collection

from matrices.routines import AESCipher
from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_image_in_cells
from matrices.routines import exists_bench_for_last_used_collection
from matrices.routines import exists_collections_for_image
from matrices.routines import get_active_collection_for_user
from matrices.routines import set_first_active_collection_for_user
from matrices.routines import set_inactive_collection_for_user
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection
from matrices.routines import get_benches_for_last_used_collection
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user
from matrices.routines import get_blog_link_post_url


WORDPRESS_SUCCESS = 'Success!'

HTTP_POST = 'POST'

NO_CREDENTIALS = ''


#
# BENCH MANIPULATION ROUTINES
#
# def delete_image(request, image_id):
#
# def detail_collection(request, collection_id):
# def view_collection(request, collection_id):
# def view_active_collection(request):
# def new_collection(request):
# def edit_collection(request, collection_id):
# def delete_collection(request, collection_id):
# def choose_collection(request, matrix_id, collection_id):
# def activate_collection(request, collection_id):
#
# def view_matrix_blog(request, matrix_id):
# def view_cell_blog(request, matrix_id, cell_id):
#
# def view_matrix(request, matrix_id):
# def new_matrix(request):
# def edit_matrix(request, matrix_id):
# def delete_matrix(request, matrix_id):
#
# def add_cell(request, matrix_id):
# def edit_cell(request, matrix_id, cell_id):
# def view_cell(request, matrix_id, cell_id):
#
# def append_column(request, matrix_id):
# def add_column_left(request, matrix_id, column_id):
# def add_column_right(request, matrix_id, column_id):
# def delete_this_column(request, matrix_id, column_id):
# def delete_last_column(request, matrix_id):
# def append_row(request, matrix_id):
# def add_row_above(request, matrix_id, row_id):
# def add_row_below(request, matrix_id, row_id):
# def delete_this_row(request, matrix_id, row_id):
# def delete_last_row(request, matrix_id):
#

#
# DELETE AN IMAGE FROM THE ACTIVE COLLECTION
#
@login_required
def delete_image(request, image_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        image = get_object_or_404(Image, pk=image_id)

        list_collections = image.collections.all()

        for collection in list_collections:

            Collection.unassign_image(image, collection)


        if not exists_image_in_cells(image):

            image.delete()


        return HttpResponseRedirect(reverse('list_collection', args=()))


#
# VIEW AN IMAGE COLLECTION DETAILS
#
@login_required
def detail_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        data.update({ 'collection_id': collection_id, 'collection': collection })

        return render(request, 'matrices/detail_collection.html', data)


#
# VIEW A COLLECTION
#
@login_required
def view_collection(request, collection_id):

    data = get_header_data(request.user)

    collection = get_object_or_404(Collection, pk=collection_id)

    collection_image_list = get_images_for_collection(collection)

    data.update({ 'collection': collection, 'collection_image_list': collection_image_list })

    return render(request, 'matrices/view_collection.html', data)


#
# VIEW THE ACTIVE COLLECTION
#
@login_required
def view_active_collection(request):

    data = get_header_data(request.user)

    collection_list = get_active_collection_for_user(request.user)

    collection = collection_list[0]

    collection_image_list = get_images_for_collection(collection)

    data.update({ 'collection': collection, 'collection_image_list': collection_image_list })

    return render(request, 'matrices/view_collection.html', data)


#
# ADD A NEW IMAGE COLLECTION
#
@login_required
def new_collection(request):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        if request.method == HTTP_POST:

            form = CollectionForm(request.POST)

            if form.is_valid:

                collection = form.save(commit=False)

                if collection.is_active:

                    if exists_active_collection_for_user(request.user):

                        set_inactive_collection_for_user(request.user)


                collection.set_owner(request.user)

                collection.save()

                return HttpResponseRedirect(reverse('list_collection', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = CollectionForm()

            data.update({ 'form': form })

        return render(request, 'matrices/new_collection.html', data)


#
# EDIT AN IMAGE COLLECTION
#
@login_required
def edit_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        if request.method == HTTP_POST:

            form = CollectionForm(request.POST, instance=collection)

            if form.is_valid:

                collection = form.save(commit=False)

                collection.set_owner(request.user)


                if collection.is_active:

                    if exists_active_collection_for_user(request.user):

                        set_inactive_collection_for_user(request.user)


                collection.save()

                return HttpResponseRedirect(reverse('list_collection', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'collection': collection })

        else:

            form = CollectionForm(instance=collection)

            data.update({ 'form': form, 'collection': collection })

        return render(request, 'matrices/edit_collection.html', data)


#
# DELETE AN IMAGE COLLECTION
#
@login_required
def delete_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        images = get_images_for_collection(collection)

        for image in images:

            Collection.unassign_image(image, collection)

            if not exists_image_in_cells(image):

                image.delete()

        if exists_bench_for_last_used_collection(collection):

            matrix_list = get_benches_for_last_used_collection(collection)

            for matrix in matrix_list:

                matrix.set_no_last_used_collection()

                matrix.save()


        set_first_active_collection_for_user(request.user)

        collection.delete()

        return HttpResponseRedirect(reverse('list_collection', args=()))


#
# CHOOSE AN IMAGE COLLECTION
#
@login_required
def choose_collection(request, matrix_id, collection_id):

    data = get_header_data(request.user)

    collection_image_list = list()

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)
        owner = get_object_or_404(User, pk=matrix.owner_id)
        user = get_object_or_404(User, pk=request.user.id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, user)

        if not authority.is_none:

            return HttpResponseRedirect(reverse('home', args=()))

        collection = get_object_or_404(Collection, pk=collection_id)

        matrix.set_last_used_collection(collection)

        matrix.save()

        return redirect('matrix', matrix_id=matrix_id)


#
# ACTIVATE AN IMAGE COLLECTION
#
@login_required
def activate_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        if collection.is_inactive:

            collection.set_active()

            if exists_active_collection_for_user(request.user):

                set_inactive_collection_for_user(request.user)

            collection.save()

    return HttpResponseRedirect(reverse('list_collections', args=()))


#
# VIEW THE BENCH BLOG ENTRY
#
@login_required
def view_matrix_blog(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        matrix_cells = matrix.get_matrix()
        columns = matrix.get_columns()
        rows = matrix.get_rows()

        blogpost = serverWordpress.get_wordpress_post(matrix.blogpost)

        if blogpost['status'] != WORDPRESS_SUCCESS:

            messages.error(request, "WordPress Error - Contact System Administrator")

        comment_list = list()

        comment_list = serverWordpress.get_wordpress_post_comments(matrix.blogpost)

        for comment in comment_list:

            if comment['status'] != WORDPRESS_SUCCESS:

                messages.error(request, "WordPress Error - Contact System Administrator")

        if request.method == HTTP_POST:

            form = CommentForm(request.POST)

            if form.is_valid:

                cd = form.cleaned_data

                comment = cd.get('comment')

                if comment != '':

                    returned_comment = serverWordpress.post_wordpress_comment(request.user.username, matrix.blogpost, comment)

                    if returned_comment['status'] != WORDPRESS_SUCCESS:

                        messages.error(request, "WordPress Error - Contact System Administrator")

                return HttpResponseRedirect(reverse('detail_matrix_blog', args=(matrix_id,)))

            else:

                messages.error(request, "Error")

        else:

            form = CommentForm()

        data.update({ 'form': form, 'matrix': matrix, 'blogpost': blogpost, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'comment_list': comment_list })

        return render(request, 'matrices/detail_matrix_blog.html', data)


#
# VIEW THE CELL BLOG ENTRY
#
@login_required
def view_cell_blog(request, matrix_id, cell_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        cell = get_object_or_404(Cell, pk=cell_id)

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        blogpost = serverWordpress.get_wordpress_post(cell.blogpost)

        if blogpost['status'] != WORDPRESS_SUCCESS:

            messages.error(request, "WordPress Error - Contact System Administrator")

        comment_list = list()

        comment_list = serverWordpress.get_wordpress_post_comments(cell.blogpost)

        for comment in comment_list:

            if comment['status'] != WORDPRESS_SUCCESS:

                messages.error(request, "WordPress Error - Contact System Administrator")

        if request.method == HTTP_POST:

            form = CommentForm(request.POST)

            if form.is_valid:

                cd = form.cleaned_data

                comment = cd.get('comment')

                if comment != '':

                    returned_comment = serverWordpress.post_wordpress_comment(request.user.username, cell.blogpost, comment)

                    if returned_comment['status'] != WORDPRESS_SUCCESS:

                        messages.error(request, "WordPress Error - Contact System Administrator")

                return HttpResponseRedirect(reverse('view_cell_blog', args=(matrix_id, cell_id)))

            else:

                messages.error(request, "Error")

        else:

            form = CommentForm()

        data.update({ 'form': form, 'matrix_id': matrix_id, 'cell': cell, 'matrix': matrix, 'blogpost': blogpost, 'comment_list': comment_list })

        return render(request, 'matrices/detail_cell_blog.html', data)


#
# DISPLAY THE BENCH!
#
@login_required
def view_matrix(request, matrix_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        owner = get_object_or_404(User, pk=matrix.owner_id)
        user = get_object_or_404(User, pk=request.user.id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, user)

        if not authority.is_none:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix_link = 'matrix_link'

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


            matrix_cells = matrix.get_matrix()

            matrix_comments = matrix.get_matrix_comments()
            matrix_cells_comments = matrix.get_matrix_cell_comments()

            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'collection_image_list': collection_image_list, 'matrix_link': matrix_link, 'authority': authority, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_cells_comments': matrix_cells_comments, 'matrix_comments': matrix_comments })

            return render(request, 'matrices/view_matrix.html', data)


#
# VIEW THE BENCH DETAILS
#
@login_required
def detail_matrix(request, matrix_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        matrix_link = get_blog_link_post_url() + matrix.blogpost

        matrix_cells = matrix.get_matrix()
        columns = matrix.get_columns()
        rows = matrix.get_rows()

        data.update({ 'matrix': matrix, 'matrix_link': matrix_link, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

        return render(request, 'matrices/detail_matrix.html', data)


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

            if form.is_valid:

                matrix = form.save(commit=False)

                rows = form.cleaned_data['rows']
                columns = form.cleaned_data['columns']

                rows = rows + 1
                columns = columns + 1

                if rows == 1:
                    rows = 2

                if columns == 1:
                    columns = 2

                if rows > 10:
                    rows = 2

                if columns > 10:
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

                    returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, matrix.title, matrix.description)

                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                        post_id = returned_blogpost['id']

                    else:

                        messages.error(request, "WordPress Error - Contact System Administrator")


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

                return HttpResponseRedirect(reverse('matrix', args=(matrix.id,)))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = NewMatrixForm()

            data.update({ 'form': form })

        return render(request, 'matrices/new_matrix.html', data)


#
# EDIT THE BENCH DETAILS
#
@login_required
def edit_matrix(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

        else:

            if request.method == HTTP_POST:

                form = MatrixForm(request.POST, instance=matrix)

                if form.is_valid:

                    matrix = form.save(commit=False)

                    if matrix.is_not_high_enough() == True:
                        matrix.set_minimum_height()

                    if matrix.is_not_wide_enough() == True:
                        matrix.set_minimum_width()

                    if matrix.is_too_high() == True:
                        matrix.set_maximum_height()

                    if matrix.is_too_wide() == True:
                        matrix.set_maximum_width()

                    post_id = ''

                    if matrix.has_no_blogpost() == True:

                        credential = get_credential_for_user(request.user)

                        if credential.has_apppwd():

                            returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, matrix.title, matrix.description)

                            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                post_id = returned_blogpost['id']

                            else:

                                messages.error(request, "WordPress Error - Contact System Administrator")

                        matrix.set_blogpost(post_id)

                    matrix.save()

                    matrix_cells = matrix.get_matrix()
                    columns = matrix.get_columns()
                    rows = matrix.get_rows()

                    data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

                    return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

                else:

                    messages.error(request, "Error")

                    data.update({ 'form': form })

            else:

                form = MatrixForm(instance=matrix)

                data.update({'form': form, 'matrix': matrix })

            return render(request, 'matrices/edit_matrix.html', data)


#
# DELETE THE BENCH
#
@login_required
def delete_matrix(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

        else:

            oldCells = Cell.objects.filter(matrix=matrix_id)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "WordPress Error - Contact System Administrator")

                if oldCell.has_image():

                    if not exists_collections_for_image(oldCell.image):

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()


            if matrix.has_blogpost() == True:

                credential = get_credential_for_user(request.user)

                if credential.has_apppwd():

                    response = serverWordpress.delete_wordpress_post(request.user.username, matrix.blogpost)

                    if response != WORDPRESS_SUCCESS:

                        messages.error(request, "WordPress Error - Contact System Administrator")

            matrix.delete()

            return HttpResponseRedirect(reverse('index', args=()))


#
# ADD A GRID OF CELLS TO A BENCH BENCH
#
@login_required
def add_cell(request, matrix_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = Matrix.objects.get(id=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            cell_list = Cell.objects.filter(matrix=matrix)

            if not cell_list:

                cell1 = Cell.create(matrix, "", "", 0, 0, "", None)
                cell2 = Cell.create(matrix, "", "", 0, 1, "", None)
                cell3 = Cell.create(matrix, "", "", 0, 2, "", None)
                cell4 = Cell.create(matrix, "", "", 1, 0, "", None)
                cell5 = Cell.create(matrix, "", "", 1, 1, "", None)
                cell6 = Cell.create(matrix, "", "", 1, 2, "", None)
                cell7 = Cell.create(matrix, "", "", 2, 0, "", None)
                cell8 = Cell.create(matrix, "", "", 2, 1, "", None)
                cell9 = Cell.create(matrix, "", "", 2, 2, "", None)

                cell1.save()
                cell2.save()
                cell3.save()
                cell4.save()
                cell5.save()
                cell6.save()
                cell7.save()
                cell8.save()
                cell9.save()

                matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# EDIT THE CELL ADDING IMAGE
#
@login_required
def edit_cell(request, matrix_id, cell_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        cell = get_object_or_404(Cell, pk=cell_id)
        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

        else:

            if request.method == HTTP_POST:

                if cell.is_header() == True:

                    form = HeaderForm(request.POST, instance=cell)

                    if form.is_valid:

                        cell = form.save(commit=False)

                        cell.set_matrix(matrix)

                        cell.save()

                        matrix.save()

                    else:

                        messages.error(request, "Error")

                        data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

                        return render(request, 'matrices/edit_cell.html', data)

                else:

                    imageOld = Image.objects.none
                    imageNew = Image.objects.none

                    if cell.has_no_image() == True:

                        form = CellForm(request.user.id, None, matrix.id, request.POST, instance=cell)

                    else:

                        form = CellForm(request.user.id, cell.image.id, matrix.id, request.POST, instance=cell)


                    if form.is_valid:

                        cell = form.save(commit=False)

                        cell.set_matrix(matrix)

                        post_id = ''

                        if cell.has_no_blogpost() == True:

                            credential = get_credential_for_user(request.user)

                            if credential.has_apppwd():

                                returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, cell.title, cell.description)

                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                    post_id = returned_blogpost['id']

                                else:

                                    messages.error(request, "WordPress Error - Contact System Administrator")

                            cell.set_blogpost(post_id)

                        cell.save()

                        matrix.save()

                    else:

                        messages.error(request, "Error")

                        data.update({ 'form': form, 'matrix': matrix, 'cell': cell })

                        return render(request, 'matrices/edit_cell.html', data)

                matrix_cells = matrix.get_matrix()
                columns = matrix.get_columns()
                rows = matrix.get_rows()

                data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

                return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

            else:

                if cell.is_header() == True:

                    form = HeaderForm(instance=cell)

                else:

                    if cell.has_no_image() == True:

                        form = CellForm(request.user.id, None, matrix.id, instance=cell)

                    else:

                        form = CellForm(request.user.id, cell.image.id, matrix.id, instance=cell)

            data.update({'form': form, 'matrix': matrix, 'cell': cell })

            return render(request, 'matrices/edit_cell.html', data)


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


#
# APPEND A COLUMN OF CELLS TO THE BENCH
#
@login_required
def append_column(request, matrix_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            nextColumn = matrix.get_column_count()
            rows = matrix.get_rows()

            for i, row in enumerate(rows):

                cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                cell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# ADD A COLUMN OF CELLS TO THE LEFT OF THE GIVEN COLUMN IN THE BENCH
#
@login_required
def add_column_left(request, matrix_id, column_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gte=column_id)
            rows = matrix.get_rows()

            for oldcell in oldCells:

                oldcell.increment_x()

                oldcell.save()

            for i, row in enumerate(rows):

                cell = Cell.create(matrix, "", "", column_id, i, "", None)

                cell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# ADD A COLUMN OF CELLS TO THE RIGHT OF THE GIVEN COLUMN IN THE BENCH
#
@login_required
def add_column_right(request, matrix_id, column_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gt=column_id)
            rows = matrix.get_rows()

            for oldcell in oldCells:

                oldcell.increment_x()

                oldcell.save()

            new_column_id = int(column_id) + 1

            for i, row in enumerate(rows):

                cell = Cell.create(matrix, "", "", new_column_id, i, "", None)

                cell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# DELETE THE GIVEN COLUMN IN THE BENCH
#
@login_required
def delete_this_column(request, matrix_id, column_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            deleteColumn = int(column_id)

            oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "WordPress Error - Contact System Administrator")


                if oldCell.has_image():

                    if not exists_collections_for_image(oldCell.image):

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()


            Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()

            moveCells = Cell.objects.filter(matrix=matrix_id, xcoordinate__gt=deleteColumn)

            for moveCell in moveCells:

                moveCell.decrement_x()

                moveCell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# DELETE THE LAST COLUMN IN THE BENCH
#
@login_required
def delete_last_column(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            deleteColumn = matrix.get_column_count()
            deleteColumn = deleteColumn - 2

            oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "WordPress Error - Contact System Administrator")


                if oldCell.has_image():

                    if not exists_collections_for_image(oldCell.image):

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()


            Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()

            moveCells = Cell.objects.filter(matrix=matrix_id, xcoordinate__gt=deleteColumn)

            for moveCell in moveCells:

                moveCell.decrement_x()

                moveCell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# APPEND A ROW OF CELLS TO THE BENCH
#
@login_required
def append_row(request, matrix_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            nextRow = matrix.get_row_count()
            columns = matrix.get_columns()

            for i, column in enumerate(columns):

                cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                cell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# ADD A ROW OF CELLS ABOVE THE GIVEN ROW IN THE BENCH
#
@login_required
def add_row_above(request, matrix_id, row_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

            matrix = Matrix.objects.get(id=matrix_id)

            oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gte=row_id)
            columns = matrix.get_columns()

            for oldcell in oldCells:

                oldcell.increment_y()

                oldcell.save()

            for i, column in enumerate(columns):

                cell = Cell.create(matrix, "", "", i, row_id, "", None)

                cell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# ADD A ROW OF CELLS BELOW THE GIVEN ROW IN THE BENCH
#
@login_required
def add_row_below(request, matrix_id, row_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gt=row_id)
            columns = matrix.get_columns()

            new_row_id = int(row_id) + 1

            for oldcell in oldCells:

                oldcell.increment_y()

                oldcell.save()

            for i, column in enumerate(columns):

                cell = Cell.create(matrix, "", "", i, new_row_id, "", None)

                cell.save()

            matrix.save()
            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# DELETE THE GIVEN ROW IN THE BENCH
#
@login_required
def delete_this_row(request, matrix_id, row_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            deleteRow = int(row_id)

            oldCells = Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "WordPress Error - Contact System Administrator")


                if oldCell.has_image():

                    if not exists_collections_for_image(oldCell.image):

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()



            Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow).delete()

            matrix.save()


            moveCells = Cell.objects.filter(matrix=matrix_id, ycoordinate__gt=deleteRow)

            for moveCell in moveCells:

                moveCell.decrement_y()

                moveCell.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))


#
# DELETE THE GIVEN ROW IN THE BENCH
#
@login_required
def delete_last_row(request, matrix_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer == True or authority.is_none == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            deleteRow = matrix.get_row_count()
            deleteRow = deleteRow - 2

            oldCells = Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

                        if response != WORDPRESS_SUCCESS:

                            messages.error(request, "WordPress Error - Contact System Administrator")


                if oldCell.has_image():

                    if not exists_collections_for_image(oldCell.image):

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()



            Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow).delete()

            matrix.save()


            moveCells = Cell.objects.filter(matrix=matrix_id, ycoordinate__gt=deleteRow)

            for moveCell in moveCells:

                moveCell.decrement_y()

                moveCell.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))
