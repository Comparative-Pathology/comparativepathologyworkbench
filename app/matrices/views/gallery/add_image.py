#!/usr/bin/python3
#
# ##
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
# This file contains the add_image view routine
# ##
#
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from matrices.models import Server

from matrices.routines import add_image_to_collection
from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_credential_for_user
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

from background.tasks import add_images_to_collection_task


#
#   ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
@login_required
def add_image(request, server_id, image_id, roi_id, path_from, identifier):

    environment = get_primary_cpw_environment()

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=server_id)

        if exists_active_collection_for_user(request.user):

            collection = get_active_collection_for_user(request.user)

            credential = get_credential_for_user(request.user)

            images_list = list()

            imagedict = {}
            imagedict["id"] = image_id

            images_list.append(imagedict)

            if environment.is_background_processing():

                collection.set_locked()
                collection.save()

                result = add_images_to_collection_task.delay_on_commit(images_list,
                                                                       request.user.id,
                                                                       server.id,
                                                                       collection.id)

            else:

                image = add_image_to_collection(credential, server, image_id, roi_id, collection.id)

                messages.success(request, 'Image ' + str(image.id) + ' ADDED to Active Collection!')

            return HttpResponseRedirect(reverse('list_images', args=(collection.id, )))

        else:

            messages.error(request, "CPW_WEB:0450 Add Image - You have no Active Image Collection; Please create "
                           "a Collection!")

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
