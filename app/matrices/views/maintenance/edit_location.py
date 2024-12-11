#!/usr/bin/python3
#
# ##
# \file         edit_location.py
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
# This file contains the edit_location view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms.locationform import LocationForm

from matrices.models import Location

from matrices.routines import get_header_data

HTTP_POST = 'POST'


#
#   EDIT A ENVIRONMENT LOCATION
#
@login_required
def edit_location(request, location_id):

    if request.user.is_superuser:

        location = Location.objects.get_or_none(id=location_id)

        if location:

            data = get_header_data(request.user)

            if request.method == HTTP_POST:

                form = LocationForm(request.POST, instance=location)

                if form.is_valid():

                    location = form.save(commit=False)

                    location.set_owner(request.user)

                    location.save()

                    messages.success(request, 'Environment Location ' + location.name + ' Updated!')

                    return HttpResponseRedirect(reverse('maintenance', args=()))

                else:

                    messages.error(request, "CPW_WEB:0140 Edit Environment Location - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0140 Edit Environment Location - Form is Invalid!")

                    data.update({'form': form,
                                 'location': location})

            else:

                form = LocationForm(instance=location)

                data.update({'form': form,
                             'location': location})

            return render(request, 'maintenance/edit_location.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
