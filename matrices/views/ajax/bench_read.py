#!/usr/bin/python3
###!
# \file         add_server.py
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

from decouple import config

from matrices.models import Matrix

from matrices.routines import get_blog_link_post_url

#
# READ A BENCH
#
@login_required()
def bench_read(request, bench_id):

    object = get_object_by_uuid_or_404(Matrix, bench_id)

    htmlString = ''

    date_created = object.created.strftime('%Y/%m/%d %H:%M')
    date_modified = object.modified.strftime('%Y/%m/%d %H:%M')

    if object.has_blogpost():

        matrix_link = get_blog_link_post_url() + object.blogpost

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
