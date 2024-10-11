#!/usr/bin/python3
###!
# \file         bench_creation_consequences.py
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
# Consequential Actions for Bench Creation
###
from __future__ import unicode_literals

from django.apps import apps

from matrices.routines import Base26


#
#   Consequential Actions for Bench Creation
#
def bench_creation_consequences(a_matrix, a_columns, a_rows, a_number_headers):

    Cell = apps.get_model('matrices', 'Cell')

    column = 0

    row_label = ''
    title_label = ''
    comment_label = ''

    while column <= a_columns:

        row = 0

        while row <= a_rows:

            if a_number_headers:

                row_label = str(row)

                title_label = ''

                if column == 0:

                    title_label = row_label

                if row == 0:

                    title_label = Base26.to_excel(column)

            else:

                row_label = str(row)

                title_label = ''
                comment_label = ''

                if column == 0:

                    comment_label = row_label

                if row == 0:

                    comment_label = Base26.to_excel(column)

            cell = Cell.create(a_matrix, title_label, comment_label, "", column, row, "", None)

            cell.save()

            row = row + 1

        column = column + 1
