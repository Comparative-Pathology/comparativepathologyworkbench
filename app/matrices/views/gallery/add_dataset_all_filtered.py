#!/usr/bin/python3
#
# ##
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
# This file contains the add_dataset_all_filtered view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Server
from matrices.models import Credential

from matrices.routines import add_image_to_collection
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

from background.tasks import add_images_to_collection_task


#
#   Add ALL the FILTERED images from a Dataset to a Collection
#
@login_required
def add_dataset_all_filtered(request, server_id, dataset_id):

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        server = Server.objects.get_or_none(id=server_id)

        if server:

            server_data = server.get_imaging_server_dataset_json(dataset_id, True)

            images_list = server_data["images"]

            if request.user.profile.has_active_collection():

                collection = request.user.profile.active_collection

                environment = get_primary_cpw_environment()

                if environment.is_background_processing():

                    collection.set_locked()
                    collection.save()

                    result = add_images_to_collection_task.delay_on_commit(images_list,
                                                                           request.user.id,
                                                                           server.id,
                                                                           collection.id)

                else:

                    imageCounter = 0

                    for image in images_list:

                        image_id = image["id"]

                        image = add_image_to_collection(request.user, server, image_id, 0, collection.id)

                        imageCounter = imageCounter + 1

                    if imageCounter > 1:

                        messages.success(request, str(imageCounter) + ' Images ADDED to Active Collection!')

                    else:

                        messages.success(request, str(imageCounter) + ' Image ADDED to Active Collection!')

                return HttpResponseRedirect(reverse('list_images', args=(collection.id, )))

            else:

                messages.error(request, "CPW_WEB:0430 Add Dataset - You have no Active Image Collection; Please "
                               "create a Collection!")

                return HttpResponseRedirect(reverse('home', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
