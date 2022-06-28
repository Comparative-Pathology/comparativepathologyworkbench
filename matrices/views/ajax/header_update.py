#!/usr/bin/python3
###!
# \file         add_server.py
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
# This file contains the AJAX bench_update view routine
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.routines import simulate_network_latency

from matrices.forms import HeaderForm

from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import simulate_network_latency

WORDPRESS_SUCCESS = 'Success!'


#
# EDIT A BENCH
#
@login_required()
def header_update(request, bench_id, header_id):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    object = get_object_by_uuid_or_404(Cell, header_id)

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = HeaderForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            object.save()

            cell_id_formatted = "CPW:" + "{:06d}".format(bench_id) + "_" + str(header_id)
            messages.success(request, 'Header ' + cell_id_formatted + ' Updated!')

    else:

        form = HeaderForm(instance=object)


    return render(request, template_name, {
        'form': form,
        'object': object
    })
