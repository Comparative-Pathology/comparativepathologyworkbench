#!/usr/bin/python3
#
# ##
# \file         list_bench_authorisation.py
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
# This file contains the list_bench_authorisation view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Authorisation
from matrices.models import Credential
from matrices.models import Matrix

from matrices.routines import get_header_data


#
#   LIST ALL PERMISSIONS FOR ALL BENCHES
#
@login_required
def list_bench_authorisation(request, matrix_id=None):

    if request.user.username == 'guest':

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        data = get_header_data(request.user)

        if matrix_id is None:

            authorisation_list = Authorisation.objects.all()

            text_flag = ' ALL Permissions, ALL Benches'
            matrix_id = ''

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            if matrix.is_locked():

                raise PermissionDenied

            authorisation_list = Authorisation.objects.filter(matrix__id=matrix_id)
            text_flag = "Permissions for Bench " + matrix.get_formatted_id()

        data.update({'matrix_id': matrix_id,
                     'text_flag': text_flag,
                     'authorisation_list': authorisation_list})

        return render(request, 'host/list_bench_authorisation.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
