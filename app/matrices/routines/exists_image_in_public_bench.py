#!/usr/bin/python3
###!
# \file         exists_image_in_public_bench.py
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
# Is there a Public Bench for a particular Image?
###
from __future__ import unicode_literals

from django.apps import apps

from django.shortcuts import get_object_or_404


#
#   Is there a Public Bench for a particular Image?
#
def exists_image_in_public_bench(image_id):

    Cell = apps.get_model('matrices', 'Cell')
    Image = apps.get_model('matrices', 'Image')

    image = Image.objects.get(birdseye_url=image_id)

    exists_bench = False

    cell_list = Cell.objects.filter(image=image)

    for cell in cell_list:

        if cell.matrix.is_public():

            exists_bench = True

            break

    return exists_bench
