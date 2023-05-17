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

import base64, hashlib
from os import urandom

from django.apps import apps
from django.db.models import Q



"""
    Consequential Actions for Bench Creation
"""
def bench_creation_consequences(a_matrix, a_columns, a_rows):

    Cell = apps.get_model('matrices', 'Cell')

    x = 0

    while x <= a_columns:

        y = 0

        while y <= a_rows:

            cell = Cell.create(a_matrix, "", "", x, y, "", None)

            cell.save()

            y = y + 1

        x = x + 1
