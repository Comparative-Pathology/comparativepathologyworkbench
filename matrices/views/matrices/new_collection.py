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
# This file contains the new_collection view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import CollectionForm

from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_title_for_collection_for_user
from matrices.routines import set_inactive_collection_for_user
from matrices.routines import get_header_data

HTTP_POST = 'POST'
NO_CREDENTIALS = ''

#
# ADD A NEW IMAGE COLLECTION
#
@login_required
def new_collection(request):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        if request.method == HTTP_POST:

            form = CollectionForm(request.POST)

            if form.is_valid():

                collection = form.save(commit=False)

                if exists_title_for_collection_for_user(request.user, collection.title):

                    messages.error(request, "Collection Title NOT Unique!")
                    form.add_error(None, "Collection Title NOT Unique!")

                    data.update({ 'form': form })

                else:

                    if collection.is_active():

                        if exists_active_collection_for_user(request.user):

                            set_inactive_collection_for_user(request.user)


                    collection.set_owner(request.user)

                    collection.save()

                    return HttpResponseRedirect(reverse('list_collections', args=()))

            else:

                messages.error(request, "Collection Form is Invalid!")
                form.add_error(None, "Collection Form is Invalid!")

                data.update({ 'form': form })

        else:

            form = CollectionForm()

            data.update({ 'form': form })

        return render(request, 'matrices/new_collection.html', data)
