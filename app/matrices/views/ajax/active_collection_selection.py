#!/usr/bin/python3
###!
# \file         active_collection_selection.py
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
# This file contains the AJAX bench_collection_update view routine
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.routines import simulate_network_latency

from matrices.forms import CollectionActiveSummarySelectionForm

from matrices.models import Matrix
from matrices.models import Collection

from matrices.routines import credential_exists
from matrices.routines import simulate_network_latency


#
# Select a Collection as the Active Collection 
#
@login_required()
def active_collection_selection(request, user_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    object = get_object_by_uuid_or_404(User, user_id)
    collection = object.profile.active_collection

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = CollectionActiveSummarySelectionForm(instance=object, initial={'active_collection': collection }, data=request.POST, request=request)

        if form.is_valid():

            cd = form.cleaned_data

            collection = cd.get('active_collection')

            object.profile.set_active_collection(collection)
            object.save()

            collection_id_formatted = "{:06d}".format(collection.id)
            messages.success(request, 'User ' + str(user_id) + ' Updated with NEW Active Collection ' + collection_id_formatted + '!')

    else:

        form = CollectionActiveSummarySelectionForm(instance=object, request=request, initial={'active_collection': collection } )

    return render(request, template_name, {
        'form': form,
        'object': object
    })
