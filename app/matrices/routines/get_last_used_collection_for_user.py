#!/usr/bin/python3
#
# ##
# \file         get_last_used_collection_for_user.py
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
# Get the Active Collection(s) for a particular User
# ##
#
from __future__ import unicode_literals


#
#   Get the Last Used Collection(s) for a particular User
#
def get_last_used_collection_for_user(a_user):

    if a_user.profile.last_used_collection is None:

        return a_user.profile.active_collection

    else:

        return a_user.profile.last_used_collection
