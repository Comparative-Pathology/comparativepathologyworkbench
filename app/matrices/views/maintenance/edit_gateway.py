#!/usr/bin/python3
#
# ##
# \file         edit_gateway.py
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
# This file contains the edit_type view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import GatewayForm

from matrices.models import Gateway

from matrices.routines import get_header_data

HTTP_POST = 'POST'


#
#   EDIT A GATEWAY
#
@login_required
def edit_gateway(request, gateway_id):

    if request.user.is_superuser:

        gateway = Gateway.objects.get_or_none(id=gateway_id)

        if gateway:

            data = get_header_data(request.user)

            if request.method == HTTP_POST:

                form = GatewayForm(request.POST, instance=gateway)

                if form.is_valid():

                    gateway = form.save(commit=False)

                    gateway.set_owner(request.user)

                    gateway.save()

                    messages.success(request, 'OMERO Gateway ' + gateway.name + ' Updated!')

                    return HttpResponseRedirect(reverse('maintenance', args=()))

                else:

                    messages.error(request, "CPW_WEB:0140 Edit OMERO Gateway - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0140 Edit OMERO Gateway - Form is Invalid!")

                    data.update({'form': form,
                                 'gateway': gateway})

            else:

                form = GatewayForm(instance=gateway)

                data.update({'form': form,
                             'gateway': gateway})

            return render(request, 'maintenance/edit_gateway.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
