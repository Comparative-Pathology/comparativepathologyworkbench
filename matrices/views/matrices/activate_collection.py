#!/usr/bin/python3
###!
# \file         activate_collection.py
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
#
# This file contains the activate_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Collection

from matrices.routines import credential_exists
from matrices.routines import collection_crud_consequences
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import set_inactive_collection_for_user


#
# ACTIVATE AN IMAGE COLLECTION
#
@login_required
def activate_collection(request, collection_id):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        collection = get_object_or_404(Collection, pk=collection_id)

        if collection.is_inactive():

            collection.set_active()

            collection_crud_consequences(request.user, collection)

            messages.success(request, 'Collection ' + "{:06d}".format(collection.id) + ' Activated!')

            collection.save()

        return HttpResponseRedirect(reverse('list_collections', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
