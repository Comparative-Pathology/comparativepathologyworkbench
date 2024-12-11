#!/usr/bin/python3
# 
# ##
# \file         header_update.py
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
# This file contains the AJAX bench_update view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.forms import HeaderForm

from matrices.models import Cell
from matrices.models import Credential
from matrices.models import Matrix

WORDPRESS_SUCCESS = 'Success!'


#
#   EDIT A BENCH
#
@login_required()
def header_update(request, bench_id, header_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=bench_id)

    if not matrix:

        raise PermissionDenied

    if matrix.is_locked():

        raise PermissionDenied

    object = Cell.objects.get_or_none(id=header_id)

    if not object:

        raise PermissionDenied

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = HeaderForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            object.save()

            messages.success(request, 'Header ' + object.get_formatted_id + ' Updated!')

    else:

        form = HeaderForm(instance=object)

    return render(request, template_name, {'form': form,
                                           'object': object})
