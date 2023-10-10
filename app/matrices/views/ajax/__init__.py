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
# AJAX INTERFACE ROUTINES
#
# def overwrite_cell(request) - MOVE
#      (Overwrites Target Cell with Source Cell, Source Cell is emptied)
# def overwrite_cell_leave(request) - COPY
#      (Overwrites Target Cell with Source Cell, Source Cell is left in place)
# def swap_cells(request) - SWAP
#      (Target Cell becomes Source Cell, Source Cell becomes Target Cell)
#
# def import_image(request)
#
# def swap_rows(request) - SWAP ROW A WITH ROW B
# def swap_columns(request) - SWAP COLUMN A WITH COLUMN B
#
# def shuffle_columns(request) - MOVE COLUMN AND PUSH EXISTING COLUMNS TO LEFT OR RIGHT
# def shuffle_rows(request) - MOVE ROW AND PUSH EXISTING ROWS TO LEFT OR RIGHT
#
###

from .active_collection_selection import active_collection_selection

from .add_cell import add_cell
from .add_columns import add_columns
from .add_rows import add_rows

from .aggregate_bench_cell_blog_read import aggregate_bench_cell_blog_read

from .autocomplete_tag import autocompleteTag

from .bench_authorisation_create import bench_authorisation_create
from .bench_authorisation_read import bench_authorisation_read
from .bench_authorisation_update import bench_authorisation_update
from .bench_authorisation_delete import bench_authorisation_delete

from .bench_blog_read import bench_blog_read
from .bench_cell_blog_read import bench_cell_blog_read

from .bench_create import bench_create
from .bench_read import bench_read
from .bench_update import bench_update
from .bench_collection_update import bench_collection_update
from .bench_delete import bench_delete

from .collection_authorisation_create import collection_authorisation_create
from .collection_authorisation_read import collection_authorisation_read
from .collection_authorisation_update import collection_authorisation_update
from .collection_authorisation_delete import collection_authorisation_delete

from .collection_create import collection_create
from .collection_read import collection_read
from .collection_update import collection_update
from .collection_delete import collection_delete
from .collection_selection import collection_selection

from .delete_cell import delete_cell

from .header_read import header_read
from .header_update import header_update

from .import_image import import_image

from .overwrite_cell import overwrite_cell
from .overwrite_cell_leave import overwrite_cell_leave

from .server_read import server_read
from .server_create_update import server_create_update
from .server_delete import server_delete

from .shuffle_columns import shuffle_columns
from .shuffle_rows import shuffle_rows

from .swap_cells import swap_cells
from .swap_columns import swap_columns
from .swap_rows import swap_rows
