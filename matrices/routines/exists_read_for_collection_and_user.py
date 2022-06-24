#!/usr/bin/python3
###!
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
# Can the supplied User VIEW the supplied Collection?
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.db.models import Q


"""
    Can the supplied User VIEW the supplied Collection?
"""
def exists_read_for_collection_and_user(a_collection, a_user):

    CollectionAuthority = apps.get_model('matrices', 'CollectionAuthority')

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    read_authority = False

    if a_user.is_superuser:

        read_authority = True

    else:

        if a_user == a_collection.owner:

            read_authority = True

        else:

            if CollectionAuthorisation.objects.filter(Q(collection=a_collection) & Q(permitted=a_user)).exists():

                collection_authorisation = CollectionAuthorisation.objects.get(Q(collection=a_collection) & Q(permitted=a_user))

                if collection_authorisation.collection_authority.is_owner():

                    read_authority = True

                if collection_authorisation.collection_authority.is_admin():

                    read_authority = True

                if collection_authorisation.collection_authority.is_viewer():

                    read_authority = True

            else:

                read_authority = False

    return read_authority
