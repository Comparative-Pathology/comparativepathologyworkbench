#!/usr/bin/python3
#
# ##
# \file         collection_authorisation_exists_for_collection_and_permitted.py
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
# Is there a Collection Authorisation for a particular Collection and a particular User?
# ##
#
from __future__ import unicode_literals

from django.apps import apps


#
#   Is there a Collection Authorisation for a particular Collection and a particular User?
#
def collection_authorisation_exists_for_collection_and_permitted(a_collection, a_user):

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    return CollectionAuthorisation.objects.filter(collection=a_collection).filter(permitted=a_user).exists()
