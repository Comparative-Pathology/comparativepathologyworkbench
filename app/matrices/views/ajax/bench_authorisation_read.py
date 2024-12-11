#!/usr/bin/python3
#
# ##
# \file         bench_authorisation_read.py
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
# This file contains the AJAX bench_authorisation_read.py view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from matrices.models import Authorisation


#
#   READ A BENCH AUTHORISATION
#
@login_required()
def bench_authorisation_read(request, authorisation_id):

    htmlString = ''

    object = Authorisation.objects.get_or_none(id=authorisation_id)

    if object:

        htmlString = '<dl class=\"standard\">'\
                     '<dt>Bench Authorisation Id</dt>'\
                     '<dd>' + str(object.id) + '</dd>'\
                     '<dt>Bench Id</dt>'\
                     '<dd>' + object.matrix.get_formatted_id() + '</dd>'\
                     '<dt>User</dt>'\
                     '<dd>' + object.permitted.username + '</dd>'\
                     '<dt>Authority</dt>'\
                     '<dd>' + object.authority.name + '</dd>'\
                     '</dl>'

    else:

        htmlString = '<h1>BENCH AUTHORISATION DOES NOT EXIST!!!</h1>'

    return HttpResponse(htmlString)
