#!/usr/bin/python3
#
# ##
# \file         unlock_collection_task.py
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
# The unlock_collection_task Task.
# ##
#
from __future__ import absolute_import

from matrices.models import Collection

from celery import shared_task


#
#   UNLOCK a Collection
#
@shared_task
def unlock_collection_task(collection_id):

    collection = Collection.objects.get(id=collection_id)

    out_message = ""

    collection.set_unlocked()
    collection.save()

    out_message = "Task unlock_collection : Collection " + collection.get_formatted_id() + " lock: " +\
        str(collection.locked) + " Complete!!"

    return out_message
