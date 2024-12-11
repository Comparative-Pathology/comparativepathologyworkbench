#!/usr/bin/python3
#
# ##
# \file         get_collection_authority_for_collection_and_user_and_requester.py
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
# Get the Collection Authorisation for a particular Collection and particular User
# ##
#
from __future__ import unicode_literals

from django.apps import apps

from django.db.models import Q


#
#   Get the Collection Authorisation for a particular Collection and particular User
#
def get_collection_authority_for_collection_and_user_and_requester(a_collection, a_user):

    CollectionAuthority = apps.get_model('matrices', 'CollectionAuthority')

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    collection_authority = CollectionAuthority.create("NONE", a_user)

    if a_user.is_superuser:

        collection_authority.set_as_admin()

    else:

        if a_user == a_collection.owner:

            collection_authority.set_as_owner()

        else:

            if CollectionAuthorisation.objects.filter(Q(collection=a_collection) & Q(permitted=a_user)).exists():

                collection_authorisation = CollectionAuthorisation.objects.get(Q(collection=a_collection) & 
                                                                               Q(permitted=a_user))

                if collection_authorisation.collection_authority.is_owner():

                    collection_authority.set_as_owner()

                if collection_authorisation.collection_authority.is_admin():

                    collection_authority.set_as_admin()

                if collection_authorisation.collection_authority.is_viewer():

                    collection_authority.set_as_viewer()

            else:

                collection_authority.set_as_none()

    return collection_authority
