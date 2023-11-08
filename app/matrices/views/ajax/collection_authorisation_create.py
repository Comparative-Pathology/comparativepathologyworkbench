#!/usr/bin/python3
###!
# \file         collection_authorisation_create.py
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
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.forms import CollectionAuthorisationForm

from matrices.models import Collection
from matrices.models import CollectionAuthority
from matrices.models import CollectionAuthorisation

from matrices.routines import collection_authorisation_create_update_consequences
from matrices.routines import credential_exists
from matrices.routines import exists_update_for_collection_and_user
from matrices.routines import simulate_network_latency


#
# ADD A COLLECTION AUTHORISATION
#
@login_required()
def collection_authorisation_create(request, collection_id=None):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


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

            if not exists_update_for_collection_and_user(collection, request.user):

                raise PermissionDenied

            object.set_collection_authority(authority)

            collection_authorisation_create_update_consequences(permitted, collection)

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

        collection = get_object_by_uuid_or_404(Collection, collection_id)

        if not exists_update_for_collection_and_user(collection, request.user):

            raise PermissionDenied


        form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(id=collection_id))
        form.fields['collection'].initial = collection_id

    form.fields['authority'] = forms.ModelChoiceField(CollectionAuthority.objects.all())
    form.fields['authority'].label_from_instance = lambda obj: "{0}".format(obj.name)

    form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
    form.fields['permitted'].label_from_instance = lambda obj: "{0}".format(obj.username)

    form.fields['collection'].label_from_instance = lambda obj: "{0:06d}, {1}".format(obj.id, obj.title)


    return render(request, template_name, {
        'form': form,
        'object': object
    })
