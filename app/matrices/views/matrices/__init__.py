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
# def delete_collection_image(request, collection_id, image_id):
#
# def activate_collection(request, collection_id):
#
# def view_all_linked_images(request):
#
# def view_matrix_blog(request, matrix_id):
# def view_cell_blog(request, matrix_id, cell_id):
#
# def view_matrix(request, matrix_id):
#
# def add_cell(request, matrix_id):
# def clear_cell(request, matrix_id, cell_id):
# def edit_cell(request, matrix_id, cell_id):
# def amend_cell(request, matrix_id, cell_id):
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
# def search_image(request, path_from, identifier):
#
# def link_images(request):
#
###

from .activate_collection import activate_collection
from .activate_in_collection import activate_in_collection
from .add_column_left import add_column_left
from .add_column_right import add_column_right
from .add_row_above import add_row_above
from .add_row_below import add_row_below
from .amend_cell import amend_cell
from .append_column import append_column
from .append_row import append_row
from .clear_cell import clear_cell
from .delete_image import delete_image
from .delete_image_link import delete_image_link
from .delete_collection_image import delete_collection_image
from .delete_last_column import delete_last_column
from .delete_last_row import delete_last_row
from .delete_this_column import delete_this_column
from .delete_this_row import delete_this_row
from .link_images import link_images
from .search_image import search_image
from .view_all_image_links import view_all_image_links
from .view_cell_blog import view_cell_blog
from .view_image_link import view_image_link
from .view_parent_image_link import view_parent_image_link
from .view_child_image_link import view_child_image_link
from .view_parent_and_child_image_links import view_parent_and_child_image_links
from .view_matrix import view_matrix
from .view_matrix_blog import view_matrix_blog
from .view_aggregated_blog import view_aggregated_blog
