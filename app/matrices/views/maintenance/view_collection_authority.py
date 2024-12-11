#!/usr/bin/python3
#
# ##
# \file         view_collection_authority.py
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
# This file contains the view_collection_authority view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import CollectionAuthority

from matrices.routines import get_header_data


#
#   VIEW A COLLECTION AUTHORITY
#
@login_required
def view_collection_authority(request, collection_authority_id):

    if request.user.is_superuser:

        collection_authority = CollectionAuthority.objects.get_or_none(id=collection_authority_id)

        if collection_authority:

            data = get_header_data(request.user)

            data.update({'collection_authority_id': collection_authority_id,
                         'collection_authority': collection_authority})

            return render(request, 'maintenance/detail_collection_authority.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
