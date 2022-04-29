#!/usr/bin/python3
###!
# \file         views_maintenance.py
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
# This file contains the new_collection_authority view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import CollectionAuthorityForm

from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# ADD A NEW COLLECTION AUTHORITY
#
@login_required
def new_collection_authority(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = CollectionAuthorityForm(request.POST)

            if form.is_valid():

                collection_authority = form.save(commit=False)

                collection_authority.set_owner(request.user)

                collection_authority.save()

                messages.success(request, 'NEW Collection Authority ' + collection_authority.name + ' Created!')

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "CPW_WEB:0170 New Collection Authority - Form is Invalid!")
                form.add_error(None, "CPW_WEB:0170 New Collection Authority - Form is Invalid!")

                data.update({ 'form': form })

        else:

            form = CollectionAuthorityForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_collection_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
