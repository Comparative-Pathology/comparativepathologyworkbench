#!/usr/bin/python3
#
# ##
# \file         add_images_to_collection_task.py
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
# The add_images_to_collection_task Task.
# ##
#
from __future__ import absolute_import

from celery import shared_task

from django.contrib.auth.models import User

from matrices.models import Server
from matrices.models import Collection

from matrices.routines import add_image_to_collection
from matrices.routines.simulate_network_latency import simulate_network_latency


#
#   Add ALL the Listed Images from a specific Server to a Collection
#
@shared_task
def add_images_to_collection_task(images_list, user_id, server_id, collection_id):

    simulate_network_latency()

    result_message = ''
    message_str = ''

    user = User.objects.get(id=user_id)
    server = Server.objects.get(id=server_id)

    collection = Collection.objects.get(id=collection_id)

    imageCounter = 0

    for image in images_list:

        image_id = image["id"]

        image_out = add_image_to_collection(user, server, image_id, 0, collection_id)

        imageCounter = imageCounter + 1

    if imageCounter > 1:

        message_str = str(imageCounter) + ' Images ADDED to Collection!'

    else:

        message_str = str(imageCounter) + ' Image ADDED to Active Collection!'

    result_message = 'ACTIVE Collection ' + collection.get_formatted_id() + ' Updated - ' + message_str

    collection.set_unlocked()
    collection.save()

    return result_message
