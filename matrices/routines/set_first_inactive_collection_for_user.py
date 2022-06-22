#!/usr/bin/python3
###!
# \file         set_first_inactive_collection_for_user.py
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
# Set the first Active Collection for a particular User to Inactive
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from matrices.routines.exists_inactive_collection_for_user import exists_inactive_collection_for_user
from matrices.routines.get_active_collection_for_user import get_active_collection_for_user


"""
    Set the first Active Collection for a particular User to Inactive
"""
def set_first_inactive_collection_for_user(a_user):

    if exists_active_collection_for_user(a_user):

        collection_list = get_active_collection_for_user(a_user)

        collection = collection_list[0]

        collection.set_inactive()

        collection.save()
