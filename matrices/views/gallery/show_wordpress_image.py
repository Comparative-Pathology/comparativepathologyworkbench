#!/usr/bin/python3
###!
# \file         show_wordpress_image.py
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
# This file contains the show_wordpress_image view routine
#
###
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from matrices.models import Server

from matrices.routines import credential_exists
from matrices.routines import get_credential_for_user
from matrices.routines import get_header_data
from matrices.routines import exists_active_collection_for_user


#
# SHOW AN IMAGE
#  FROM A WORDPRESS SERVER
#
@login_required()
def show_wordpress_image(request, server_id, image_id):
    """
    Show an image
    """

    if request.user.username == 'guest':

        raise PermissionDenied


    data = get_header_data(request.user)

    if credential_exists(request.user):

        image_flag = False

        credential = get_credential_for_user(request.user)

        if exists_active_collection_for_user(request.user):

            image_flag = True

        data.update({ 'image_flag': image_flag, 'add_from': "show_wordpress_image" })

        server = get_object_or_404(Server, pk=server_id)

        if server.is_wordpress():

            server_data = server.get_wordpress_image_json(credential, image_id)

            data.update(server_data)

            return render(request, 'gallery/show_wordpress_image.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
