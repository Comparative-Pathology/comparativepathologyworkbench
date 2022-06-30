#!/usr/bin/python3
###!
# \file         list_user_bench_authorisation.py
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
# This file contains the list_user_bench_authorisation view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matrices.models import Authorisation

from matrices.routines import credential_exists
from matrices.routines import get_header_data


#
# LIST ALL PERMISSIONS FOR ALL BENCHES FOR A USER
#
@login_required
def list_user_bench_authorisation(request, user_id):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        authorisation_list = Authorisation.objects.filter(matrix__owner=user_id)
        user = get_object_or_404(User, pk=user_id)

        text_flag = " ALL Bench Permissions for " + user.username
        matrix_id = ''

        data.update({ 'matrix_id': matrix_id, 'text_flag': text_flag, 'authorisation_list': authorisation_list })

        return render(request, 'host/list_bench_authorisation.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
