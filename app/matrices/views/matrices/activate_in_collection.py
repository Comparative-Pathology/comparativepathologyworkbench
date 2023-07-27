#!/usr/bin/python3
###!
# \file         activate_in_collection.py
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

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.forms import SearchUrlForm

from matrices.models import Collection
from matrices.models import CollectionSummary

from matrices.routines import credential_exists


#
# ACTIVATE AN IMAGE COLLECTION on View Collection Page
#
@login_required
def activate_in_collection(request, collection_id):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied


    if credential_exists(request.user):

        collection = get_object_or_404(Collection, pk=collection_id)

        request.user.profile.set_active_collection(collection)
        request.user.save()

        messages.success(request, 'Collection ' + "{:06d}".format(collection.id) + ' Activated!')

        return HttpResponseRedirect(reverse('list_images', args=(collection_id, )))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
