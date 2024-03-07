#!/usr/bin/python3
###!
# \file         add_image.py
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
# This file contains the add_image view routine
#
###
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from matrices.models import Server

from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_credential_for_user
from matrices.routines import add_image_to_collection


#
# ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
@login_required
def add_image(request, server_id, image_id, roi_id, path_from, identifier):

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=server_id)

        if exists_active_collection_for_user(request.user):

            credential = get_credential_for_user(request.user)

            image = add_image_to_collection(credential, server, image_id, roi_id)

            messages.success(request, 'Image ' + str(image.id) + ' ADDED to Active Collection!')

        else:

            messages.error(request, "CPW_WEB:0450 Add Image - You have no Active Image Collection; Please create a Collection!")

            return HttpResponseRedirect(reverse('home', args=()))

        if server.is_omero547():

            if path_from == "show_image":

                return HttpResponseRedirect(reverse('webgallery_show_image', args=(server_id, image_id)))

            if path_from == "show_dataset":

                return HttpResponseRedirect(reverse('webgallery_show_dataset', args=(server_id, identifier)))

        else:

            if server.is_wordpress():

                return HttpResponseRedirect(reverse('webgallery_show_wordpress_image', args=(server_id, image_id)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
