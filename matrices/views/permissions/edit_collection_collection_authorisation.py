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
# This file contains the edit_collection_collection_authorisation view routine
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matrices.forms import CollectionAuthorisationForm

from matrices.models import Collection
from matrices.models import CollectionAuthorisation
from matrices.models import CollectionAuthority

from matrices.routines import collection_authorisation_exists_for_collection_and_permitted
from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# EDIT A COLLECTION AUTHORISATION FOR A GIVEN COLLECTION
#
@login_required
def edit_collection_collection_authorisation(request, collection_id, collection_authorisation_id):

    data = get_header_data(request.user)

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)

    if request.method == HTTP_POST:

        next_page = request.POST.get('next', '/')

        form = CollectionAuthorisationForm(request.POST, instance=collection_authorisation)

        if form.is_valid():

            collection_authorisation = form.save(commit=False)

            collection_authorisation.set_collection_authority(form.cleaned_data['authority'])

            if collection_authorisation_exists_for_collection_and_permitted(collection_authorisation.collection, collection_authorisation.permitted):

                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection_authorisation.collection) & Q(permitted=collection_authorisation.permitted))

                if collection_authorisation_old.collection_authority != collection_authorisation.collection_authority:

                    collection_authorisation_old.collection_authority = collection_authorisation.collection_authority

                    collection_authorisation_old.save()

            else:

                collection_authorisation.save()

            return HttpResponseRedirect(next_page)

        else:

            text_flag = " for Bench CPW:" + format(int(collection_id), '06d')

            messages.error(request, "Collection Authorisation Form is Invalid!")
            form.add_error(None, "Collection Authorisation Form is Invalid!")

            data.update({ 'text_flag': text_flag, 'form': form, 'collection_authorisation': collection_authorisation })

    else:

        text_flag = " for Bench CPW:" + format(int(collection_id), '06d')

        form = CollectionAuthorisationForm(instance=collection_authorisation)

        form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(id=collection_id))
        form.fields['collection'].initial = collection_id

        form.fields['authority'] = forms.ModelChoiceField(CollectionAuthority.objects.all())
        form.fields['authority'].initial = collection_authorisation.collection_authority.id

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
        form.fields['permitted'].initial = collection_authorisation.permitted.id

        data.update({ 'text_flag': text_flag, 'form': form, 'collection_authorisation': collection_authorisation })

    return render(request, 'permissions/edit_collection_authorisation.html', data)
