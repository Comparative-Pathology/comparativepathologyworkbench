#!/usr/bin/python3
#
# ##
# \file         server_read.py
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
# This file contains the AJAX server_read view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from matrices.models import Server


#
#   Read AN IMAGE SERVER
#
@login_required()
def server_read(request, server_id):

    htmlString = ''

    object = Server.objects.get_or_none(id=server_id)

    if object:

        htmlString = '<dl class=\"standard\">'\
            '<dt>Name</dt>'\
            '<dd>' + object.name + '</dd>'\
            '<dt>URL</dt>'\
            '<dd>' + object.url_server + '</dd>'\
            '<dt>Type</dt>'\
            '<dd>' + object.type.name + '</dd>'\
            '<dt>Accessible</dt>'\
            '<dd>' + str(object.accessible) + '</dd>'\
            '</dl>'

    else:

        htmlString = '<h1>IMAGE SERVER DOES NOT EXIST!!!</h1>'

    return HttpResponse(htmlString)
