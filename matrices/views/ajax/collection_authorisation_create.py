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
# This file contains the AJAX collection_authorisation_create view routine
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.forms import CollectionAuthorisationForm

from matrices.models import Collection
from matrices.models import CollectionAuthority
from matrices.models import CollectionAuthorisation

from matrices.routines import simulate_network_latency
from matrices.routines import collection_authorisation_create_update_consequences


#
# ADD A COLLECTION AUTHORISATION
#
@login_required()
def collection_authorisation_create(request, collection_id=None):

    object = None

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = CollectionAuthorisationForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            permitted = form.cleaned_data['permitted']
            collection = form.cleaned_data['collection']
            authority = form.cleaned_data['authority']

            object.set_collection_authority(authority)

            collection_authorisation_create_update_consequences(permitted, collection, authority)

            object.save()

            messages.success(request, 'Collection Authorisation ' + str(object.id) + ' ADDED for Collection '+ '{num:06d}'.format(num=object.collection.id))

    else:

        form = CollectionAuthorisationForm()


    if collection_id is None:

        if request.user.is_superuser:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.all())

        else:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(owner=request.user))

    else:

        form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(id=collection_id))
        form.fields['collection'].initial = collection_id

    form.fields['authority'] = forms.ModelChoiceField(CollectionAuthority.objects.all())

    form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))


    return render(request, template_name, {
        'form': form,
        'object': object
    })
