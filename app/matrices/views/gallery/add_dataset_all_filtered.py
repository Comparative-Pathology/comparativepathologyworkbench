#!/usr/bin/python3
###!
# \file         add_dataset_all_filtered.py
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
# This file contains the add_dataset_all_filtered view routine
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
from matrices.routines import add_image_to_collection

#
# Add ALL the FILTERED images from a Dataset to a Collection
#
@login_required
def add_dataset_all_filtered(request, server_id, dataset_id):

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=server_id)

        server_data = server.get_imaging_server_dataset_json(dataset_id, True)

        images_list = server_data["images"]

        if exists_active_collection_for_user(request.user):

            imageCounter = 0

            for image in images_list:

                image_id = image["id"]

                image = add_image_to_collection(request.user, server, image_id, 0)

                imageCounter = imageCounter + 1

            if imageCounter > 1:

                messages.success(request, str(imageCounter) + ' Images ADDED to Active Collection!')

            else:

                messages.success(request, str(imageCounter) + ' Image ADDED to Active Collection!')

        else:

            messages.error(request, "CPW_WEB:0430 Add Dataset - You have no Active Image Collection; Please create a Collection!")

            return HttpResponseRedirect(reverse('home', args=()))

        return HttpResponseRedirect(reverse('webgallery_show_dataset', args=(server_id, dataset_id)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
