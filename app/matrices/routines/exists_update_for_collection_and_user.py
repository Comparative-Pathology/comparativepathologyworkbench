#!/usr/bin/python3
# 
# ##
# \file         exists_update_for_collection_and_user.py
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
# Can the supplied User UPDATE the supplied Collection?
# ##
#
from __future__ import unicode_literals

from django.apps import apps

from django.db.models import Q


#
#   Get the Collection Authorisation for a particular Collection and particular User
#
def exists_update_for_collection_and_user(a_collection, a_user):

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    update_authority = False

    if a_user.is_superuser:

        update_authority = True

    else:

        if a_user == a_collection.owner:

            update_authority = True

        else:

            if CollectionAuthorisation.objects.filter(Q(collection=a_collection) & Q(permitted=a_user)).exists():

                collection_authorisation = CollectionAuthorisation.objects.get(Q(collection=a_collection) & 
                                                                               Q(permitted=a_user))

                if collection_authorisation.collection_authority.is_owner():

                    update_authority = True

                if collection_authorisation.collection_authority.is_admin():

                    update_authority = True

                if collection_authorisation.collection_authority.is_viewer():

                    update_authority = False

            else:

                update_authority = False

    return update_authority
