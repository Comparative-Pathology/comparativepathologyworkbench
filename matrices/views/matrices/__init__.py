#!/usr/bin/python3
###!
# \file         __init__.py
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
# BENCH MANIPULATION ROUTINES
#
# def delete_image(request, image_id):
#
# def detail_collection(request, collection_id):
# def view_collection(request, collection_id):
# def view_active_collection(request):
# def view_all_collections(request):
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
# def detail_matrix(request, matrix_id):
# def new_matrix(request):
# def edit_matrix(request, matrix_id):
# def delete_matrix(request, matrix_id):
#
# def add_cell(request, matrix_id):
# def edit_cell(request, matrix_id, cell_id):
# def update_cell(request, matrix_id, cell_id):
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
# def search_image(request, path_from, identifier)):
#
###

from .delete_image import delete_image
from .detail_collection import detail_collection
from .view_collection import view_collection
from .view_active_collection import view_active_collection
from .view_all_collections import view_all_collections
from .new_collection import new_collection
from .edit_collection import edit_collection
from .delete_collection import delete_collection
from .choose_collection import choose_collection
from .activate_collection import activate_collection
from .view_matrix_blog import view_matrix_blog
from .view_cell_blog import view_cell_blog
from .view_matrix import view_matrix
from .detail_matrix import detail_matrix
from .new_matrix import new_matrix
from .edit_matrix import edit_matrix
from .delete_matrix import delete_matrix
from .add_cell import add_cell
from .edit_cell import edit_cell
from .update_cell import update_cell
from .view_cell import view_cell
from .append_column import append_column
from .add_column_left import add_column_left
from .add_column_right import add_column_right
from .delete_this_column import delete_this_column
from .delete_last_column import delete_last_column
from .append_row import append_row
from .add_row_above import add_row_above
from .add_row_below import add_row_below
from .delete_this_row import delete_this_row
from .delete_last_row import delete_last_row
from .search_image import search_image
