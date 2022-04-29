#!/usr/bin/python3
###!
# \file         views_gallery.py
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

from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import add_image_to_collection

NO_CREDENTIALS = ''

#
# ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
@login_required
def add_dataset(request, server_id, dataset_id):

    data = get_header_data(request.user)

    if not exists_active_collection_for_user(request.user):

        return HttpResponseRedirect(reverse('home', args=()))

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if exists_active_collection_for_user(request.user):

            image_ids = request.POST.getlist('checks[]')

            imageCounter = 0

            for image_id in image_ids:

                image = add_image_to_collection(request.user, server, image_id, 0)

                imageCounter = imageCounter + 1

            if imageCounter > 1:

                messages.success(request, str(imageCounter) + ' Images ADDED to Active Collection!')

            else:

                messages.success(request, str(imageCounter) + ' Image ADDED to Active Collection!')

        else:

            messages.error(request, "CPW_WEB:0670 Add Dataset - You have no Active Image Collection; Please create a Collection!")

        return HttpResponseRedirect(reverse('webgallery_show_dataset', args=(server_id, dataset_id)))
