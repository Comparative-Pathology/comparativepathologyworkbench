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

from .overwrite_cell import overwrite_cell
from .overwrite_cell_leave import overwrite_cell_leave
from .swap_cells import swap_cells
from .import_image import import_image
from .swap_rows import swap_rows
from .swap_columns import swap_columns
from .shuffle_columns import shuffle_columns
from .shuffle_rows import shuffle_rows
