#!/usr/bin/python3
#
# ##
# \file         home.py
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
# This file contains the home view routine
# ##
#
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.models import Credential

from matrices.routines import get_header_data
from matrices.routines import get_or_none_user
from matrices.routines import is_request_ajax


#
#   HOME VIEW
#
def home(request):

    if is_request_ajax(request):

        raise PermissionDenied

    credentialExists = False

    user = get_or_none_user(request.user.id)

    if user:

        credential = Credential.objects.get_or_none(username=request.user.username)

        if credential:

            credentialExists = True

    data = get_header_data(request.user)

    data.update({'credentialExists': credentialExists, })

    return render(request, 'host/home.html', data)
