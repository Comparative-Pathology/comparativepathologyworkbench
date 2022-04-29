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
# This file contains the new_collection_authorisation view routine
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from matrices.forms import CollectionAuthorisationForm

from matrices.models import Collection
from matrices.models import CollectionAuthority
from matrices.models import CollectionAuthorisation

from matrices.routines import collection_authorisation_exists_for_collection_and_permitted
from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# CREATE A NEW COLLECTION AUTHORISATION
#
@login_required
def new_collection_authorisation(request):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:

        next_page = request.POST.get('next', '/')

        form = CollectionAuthorisationForm(request.POST)

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

            messages.success(request, 'NEW Collection Authorisation ' + str(collection_authorisation.id) + ' Created!')

            return HttpResponseRedirect(next_page)

        else:

            text_flag = ''

            messages.error(request, "CPW_WEB:0580 New Collection Authorisation - Form is Invalid!")
            form.add_error(None, "CPW_WEB:0580 New Collection Authorisation - Form is Invalid!")

            data.update({ 'text_flag': text_flag, 'form': form })

    else:

        text_flag = ''

        form = CollectionAuthorisationForm()

        if request.user.is_superuser:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.all())

        else:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(owner=request.user))

        form.fields['authority'] = forms.ModelChoiceField(CollectionAuthority.objects.all())

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form })

    return render(request, 'permissions/new_collection_authorisation.html', data)
