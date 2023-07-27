#!/usr/bin/python3
###!
# \file         collection_create.py
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
# This file contains the AJAX collection_authorisation_create view routine
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.forms import CollectionCreateForm

from matrices.models import Collection

from matrices.routines import credential_exists
from matrices.routines import get_collection_count_for_user
from matrices.routines import simulate_network_latency
from matrices.routines import get_primary_cpw_environment

#
# ADD A COLLECTION
#
@login_required()
def collection_create(request, collection_id=None):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    object = None

    template_name = 'frontend_forms/generic_form_inner.html'
    environment = get_primary_cpw_environment()

    if request.method == 'POST':

        simulate_network_latency()

        form = CollectionCreateForm(instance=object, data=request.POST, request=request)

        if get_collection_count_for_user(request.user) >= environment.maximum_collection_count and request.user.username == 'guest':

            messages.error(request, "CPW_WEB:0610 New Collection  - Too Many Collections for Guest User!")
            form.add_error(None, "CPW_WEB:0610 New Collection  - Too Many Collections for Guest User!")
        
        else:

            if form.is_valid():

                object = form.save(commit=False)

                object.set_owner(request.user)

                object.save()

                activate_collection = form.cleaned_data['activate_collection']

                if activate_collection == True:

                    request.user.profile.set_active_collection(object)
                    request.user.save()

                messages.success(request, 'NEW Collection ' + "{:06d}".format(object.id) + ' Created!')

    else:

        form = CollectionCreateForm(request=request)


    return render(request, template_name, {
        'form': form,
        'object': object
    })
