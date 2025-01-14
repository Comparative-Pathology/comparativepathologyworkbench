#!/usr/bin/python3
#
# ##
# \file         get_or_none_tag.py
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
# Return the Tag OR None for a particular Tag Id
# ##
#
from __future__ import unicode_literals

from taggit.models import Tag


#
#   Return the Tag OR None for a particular Tag Id
#
def get_or_none_tag(tag_id):

    tag = None

    if Tag.objects.filter(id=tag_id).exists():

        tag = Tag.objects.get(id=tag_id)

    return tag