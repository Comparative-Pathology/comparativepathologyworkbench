#!/usr/bin/python3
###!
# \file         bench_read.py
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
# This file contains the AJAX bench_read.py view routine
#
###
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.models import Matrix

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

#
# READ A BENCH
#
@login_required()
def bench_read(request, bench_id):

    environment = get_primary_cpw_environment()

    object = get_object_by_uuid_or_404(Matrix, bench_id)

    htmlString = ''

    date_created = object.created.strftime(environment.date_format)
    date_modified = object.modified.strftime(environment.date_format)
    time_created = object.created.strftime(' %H:%M')
    time_modified = object.modified.strftime(' %H:%M')

    if object.has_blogpost():

        matrix_link = environment.get_a_link_url_to_post() + object.blogpost

        htmlString = '<dl class=\"standard\">'\
            '<dt>Title</dt>'\
            '<dd>' + object.title + '</dd>'\
            '<dt>Description</dt>'\
            '<dd>' + object.description + '</dd>'\
            '<dt>Cell Height</dt>'\
            '<dd>' + str(object.height) + '</dd>'\
            '<dt>Cell Width</dt>'\
            '<dd>' + str(object.width) + '</dd>'\
            '<dt>Owner</dt>'\
            '<dd>' + object.owner.username + ' (' + object.owner.first_name + ' ' + object.owner.last_name + ')</dd>'\
            '<dt>Created</dt>'\
            '<dd>' + date_created + time_created + '</dd>'\
            '<dt>Last Modified</dt>'\
            '<dd>' + date_modified + time_modified + '</dd>'\
            '<dt>Blog Post</dt>'\
            '<dd><a class=\"btn btn-default\" href=\"' + matrix_link + '\" role=\"button\" target=\"_blank\"><button class=\"button button-view\">View Blog Post ' + object.blogpost + ' &raquo;</button></a></dd>'\
            '</dl>'

    else:

        htmlString = '<dl class=\"standard\">'\
            '<dt>Title</dt>'\
            '<dd>' + object.title + '</dd>'\
            '<dt>Description</dt>'\
            '<dd>' + object.description + '</dd>'\
            '<dt>Cell Height</dt>'\
            '<dd>' + str(object.height) + '</dd>'\
            '<dt>Cell Width</dt>'\
            '<dd>' + str(object.width) + '</dd>'\
            '<dt>Owner</dt>'\
            '<dd>' + object.owner.username + ' (' + object.owner.first_name + ' ' + object.owner.last_name + ')</dd>'\
            '<dt>Created</dt>'\
            '<dd>' + date_created + '</dd>'\
            '<dt>Last Modified</dt>'\
            '<dd>' + date_modified + '</dd>'\
            '</dl>'

    return HttpResponse(htmlString)
