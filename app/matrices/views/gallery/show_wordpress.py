#!/usr/bin/python3
#
# ##
# \file         show_wordpress.py
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
# This file contains the show_wordpress view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Credential
from matrices.models import Server

from matrices.routines import get_header_data


#
#   SHOW THE AVAILABLE IMAGES
#    FROM A WORDPRESS SERVER
#
@login_required()
def show_wordpress(request, server_id, page_id):

    if request.user.username == 'guest':

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        server = Server.objects.get_or_none(id=server_id)

        if server:

            if server.is_wordpress():

                server_data = server.get_wordpress_json(credential, page_id)

                data = get_header_data(request.user)

                data.update(server_data)

                return render(request, 'gallery/show_wordpress.html', data)

            else:

                return HttpResponseRedirect(reverse('home', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
