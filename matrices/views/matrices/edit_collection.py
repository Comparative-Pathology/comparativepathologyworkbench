#!/usr/bin/python3
###!
# \file         views_matrices.py
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
# This file contains the edit_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import CollectionForm

from matrices.models import Collection

from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import set_inactive_collection_for_user

NO_CREDENTIALS = ''
HTTP_POST = 'POST'

#
# EDIT AN IMAGE COLLECTION
#
@login_required
def edit_collection(request, collection_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        collection = get_object_or_404(Collection, pk=collection_id)

        if request.method == HTTP_POST:

            form = CollectionForm(request.POST, instance=collection)

            if form.is_valid():

                collection = form.save(commit=False)

                collection.set_owner(request.user)


                if collection.is_active():

                    if exists_active_collection_for_user(request.user):

                        set_inactive_collection_for_user(request.user)


                collection.save()

                return HttpResponseRedirect(reverse('list_collections', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'collection': collection })

        else:

            form = CollectionForm(instance=collection)

            data.update({ 'form': form, 'collection': collection })

        return render(request, 'matrices/edit_collection.html', data)
