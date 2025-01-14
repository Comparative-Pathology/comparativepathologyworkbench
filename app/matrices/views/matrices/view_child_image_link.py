#!/usr/bin/python3
#
# ##
# \file         view_child_image_link.py
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
# This file contains the view_child_image_link view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.models import Credential
from matrices.models import Image

from matrices.routines import get_header_data
from matrices.routines import is_request_ajax


#
#   VIEW ALL IMAGE LINKS for the Child Image
#
@login_required
def view_child_image_link(request, image_child_id):

    if is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if request.user.username == 'guest':

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        image_child = Image.objects.get_or_none(id=image_child_id)

        if image_child:

            data = get_header_data(request.user)

            selected_collection = request.user.profile.active_collection

            image_link_list = list()

            if image_child.exists_child_image_links():

                image_link_list = image_child.get_child_image_links()

            data.update({'image_link_list': image_link_list,
                         'image_child': image_child,
                         'selected_collection': selected_collection})

            return render(request, 'matrices/view_child_image_links.html', data)

        else:

            raise PermissionDenied

    else:

        raise PermissionDenied
