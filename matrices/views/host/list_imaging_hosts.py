#!/usr/bin/python3
###!
# \file         list_imaging_hosts.py
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
# This file contains the list_imaging_hosts view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from matrices.forms import SearchUrlForm

from matrices.routines import credential_exists
from matrices.routines import get_header_data


#
# LIST SERVERS
#
@login_required
def list_imaging_hosts(request):

    data = get_header_data(request.user)

    readBoolean = False
    updateBoolean = False

    if credential_exists(request.user):

        readBoolean = True

        if request.user.is_superuser:

            updateBoolean = True

        form = SearchUrlForm()

        data.update({ 'form': form, 'search_from': "list_imaging_hosts", 'readBoolean': readBoolean, 'updateBoolean': updateBoolean })

        return render(request, 'host/list_imaging_hosts.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
