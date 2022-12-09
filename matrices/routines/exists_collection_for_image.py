#!/usr/bin/python3
###!
# \file         exists_collection_for_image.py
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
# Get A Collection for an Image
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom


"""
    Is there a Collection for an Image
"""
def exists_collection_for_image(a_collection, a_image):

    collection_list = a_image.collections.all()

    collection_exist = False

    if not collection_list:

        collection_exist = False
    
    else:

        for collection in collection_list:

            if collection == a_collection:

                collection_exist = True


    return collection_exist
