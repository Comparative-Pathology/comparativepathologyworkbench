#!/usr/bin/python3
#
# ##
# \file         collection_authorisation_create_update_consequences.py
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
# Consequential Actions for Collection Authorisation Creates and Updates
# ##
#
from __future__ import unicode_literals

from django.db.models import Q

from django.apps import apps

from matrices.routines import collection_authorisation_exists_for_collection_and_permitted


#
#   Consequential Actions for Collection Authorisation Creates and Updates
#
def collection_authorisation_create_update_consequences(a_permitted, a_collection):

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    if collection_authorisation_exists_for_collection_and_permitted(a_collection, a_permitted):

        collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=a_collection) &
                                                                           Q(permitted=a_permitted))

        collection_authorisation_old.delete()
