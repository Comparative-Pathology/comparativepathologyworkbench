#!/usr/bin/python3
###!
# \file         add_server.py
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
# This file contains the AJAX collection_authorisation_update view routine
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.forms import CollectionForm

from matrices.models import Collection

from matrices.routines import simulate_network_latency
from matrices.routines import collection_crud_consequences

#
# EDIT A COLLECTION AUTHORISATION
#
@login_required()
def collection_update(request, collection_id):

    object = get_object_by_uuid_or_404(Collection, collection_id)

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = CollectionForm(instance=object, data=request.POST, request=request)

        if form.is_valid():

            object = form.save(commit=False)

            collection_crud_consequences(request.user, object)

            object.set_owner(request.user)

            object.save()

            messages.success(request, 'EXISTING Collection ' + "{:06d}".format(object.id) + ' Updated!')

    else:

        form = CollectionForm(instance=object, request=request)


    return render(request, template_name, {
        'form': form,
        'object': object
    })
