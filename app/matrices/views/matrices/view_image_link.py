#!/usr/bin/python3
#
# ##
# \file         view_image_link.py
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
# This file contains the view_image_link view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.models import Credential
from matrices.models import ImageLink

from matrices.routines import get_header_data


#
#   VIEW ALL IMAGE LINKS
#
@login_required
def view_image_link(request, image_link_id):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if request.user.username == 'guest':

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        selected_collection = request.user.profile.active_collection

        image_link = ImageLink.objects.get_or_none(id=image_link_id)

        if image_link:

            data = get_header_data(request.user)

            data.update({'image_link': image_link,
                         'selected_collection': selected_collection})

            return render(request, 'matrices/view_image_link.html', data)

        else:

            raise PermissionDenied

    else:

        raise PermissionDenied
