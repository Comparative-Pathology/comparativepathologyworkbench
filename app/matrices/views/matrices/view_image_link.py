#!/usr/bin/python3
###!
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
#
# This file contains the view_image_link view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matrices.models import ImageLink

from matrices.routines import credential_exists
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data

#
# VIEW ALL IMAGE LINKS
#
@login_required
def view_image_link(request, image_link_id):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if request.user.username == 'guest':

        raise PermissionDenied


    if credential_exists(request.user):

        data = get_header_data(request.user)

        selected_collection = get_active_collection_for_user(request.user)

        image_link = get_object_or_404(ImageLink, pk=image_link_id)

        data.update({ 'image_link': image_link, 'selected_collection': selected_collection })

        return render(request, 'matrices/view_image_link.html', data)

    else:

        raise PermissionDenied
