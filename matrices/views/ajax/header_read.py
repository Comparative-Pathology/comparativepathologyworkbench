#!/usr/bin/python3
###!
# \file         header_read.py
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
# This file contains the AJAX header_read.py view routine
#
###
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.models import Cell


#
# READ A HEADER CELL
#
@login_required()
def header_read(request, bench_id, header_id):

    object = get_object_by_uuid_or_404(Cell, header_id)

    htmlString = ''
    out_title = ''
    out_description = ''

    if object.title == '':
        out_title = 'No Title'
    else:
        out_title = object.title

    if object.description == '':
        out_description = 'No Description'
    else:
        out_description = object.description

    htmlString = '<dl class=\"standard\">'\
            '<dt>Title</dt>'\
            '<dd>' + out_title + '</dd>'\
            '<dt>Description</dt>'\
            '<dd>' + out_description + '</dd>'\
            '</dl>'

    return HttpResponse(htmlString)
