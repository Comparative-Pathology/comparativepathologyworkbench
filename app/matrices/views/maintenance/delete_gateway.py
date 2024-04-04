#!/usr/bin/python3
###!
# \file         delete_gateway.py
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
# This file contains the delete_gateway view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Gateway

from matrices.routines import exists_environment_for_gateway


#
#   DELETE AN OMERO GATEWAY
#
@login_required
def delete_gateway(request, gateway_id):

    if request.user.is_superuser:

        gateway = get_object_or_404(Gateway, pk=gateway_id)

        if exists_environment_for_gateway(gateway):

            messages.error(request, 'CPW_WEB:0510 OMERO Gateway ' + gateway.name +
                           ' NOT Deleted - Environments still exist!')

        else:

            messages.success(request, 'OMERO Gateway ' + gateway.name + ' Deleted!')

            gateway.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
