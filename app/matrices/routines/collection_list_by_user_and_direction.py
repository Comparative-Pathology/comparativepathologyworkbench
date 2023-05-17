#!/usr/bin/python3
###!
# \file         collection_list_by_user_and_direction.py
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
# Get All Collections for a particular User
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.contrib.auth.models import User

from django.apps import apps

from django.db.models import Q


"""
    Get All Collections for a particular User
"""
def collection_list_by_user_and_direction(a_user, a_direction, a_query_title, a_query_description, a_query_owner, a_query_authority):

    CollectionSummary = apps.get_model('matrices', 'CollectionSummary')
    CollectionAuthority = apps.get_model('matrices', 'CollectionAuthority')

    str_query_authority = ''
    str_query_owner = ''

    if a_query_description != '':
        a_query_description = a_query_description

    if a_query_authority != '':

        collectionauthority = CollectionAuthority.objects.get(pk=int(a_query_authority))
        str_query_authority = collectionauthority.name

    if a_query_owner != '':

        user = User.objects.get(pk=int(a_query_owner))
        str_query_owner = user.username

    sort_parameter = 'collection_id'

    if a_direction == '':

        sort_parameter = 'collection_id'

    else:

        sort_parameter = a_direction

    queryset = []

    if a_user.is_superuser:

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN')).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN')).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN')).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN')).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_description__icontains=a_query_description)).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_description__icontains=a_query_description)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN') & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

    else:

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username)).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_description__icontains=a_query_description)).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_description__icontains=a_query_description)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username) & Q(collection_title__icontains=a_query_title) & Q(collection_description__icontains=a_query_description)).filter(collection_owner=str_query_owner).filter(collection_authorisation_authority=str_query_authority).order_by(sort_parameter)

    return queryset
