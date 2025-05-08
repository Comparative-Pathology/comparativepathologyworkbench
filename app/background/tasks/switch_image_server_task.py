#!/usr/bin/python3
#
# ##
# \file         switch_image_server_task.py
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
# The switch_image_server_task Task.
# ##
#
from __future__ import absolute_import

from matrices.models import Image
from matrices.models import Server

from celery import shared_task


#
#   LOCK a Bench
#
@shared_task
def switch_image_server_task(image_id, image_name, image_server_id):

    image = Image.objects.get(id=image_id)
    server = Server.objects.get(id=image_server_id)

    out_message = ""

    image.name = image_name
    image.server = server
    image.save()

    out_message = "Task switch_image_server_task: Image " + str(image.id) + \
                  " named: " + str(image.name) + \
                  " has NEW server: " + str(image.server.name)

    return out_message
