#!/usr/bin/python3
###!
# \file         views_permissions.py
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
# This file contains the view_collection_authorisation view routine
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matrices.models import CollectionAuthorisation

from matrices.routines import get_header_data

#
# VIEW THE COLLECTION AUTHORISATION
#
@login_required
def view_collection_authorisation(request, collection_authorisation_id):

    data = get_header_data(request.user)

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)

    data.update({ 'collection_authorisation_id': collection_authorisation_id, 'collection_authorisation': collection_authorisation })

    return render(request, 'permissions/detail_collection_authorisation.html', data)
