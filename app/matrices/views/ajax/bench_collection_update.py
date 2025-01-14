#!/usr/bin/python3
# 
# ##
# \file         bench_collection_update.py
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
# This file contains the AJAX bench_collection_update view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.forms import CollectionSummarySelectionForm

from matrices.models import Credential
from matrices.models import Matrix

from matrices.routines import is_request_ajax


#
#   EDIT A BENCH
#
@login_required()
def bench_collection_update(request, bench_id):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    object = Matrix.objects.get_or_none(id=bench_id)

    if not object:

        raise PermissionDenied

    collection = object.last_used_collection

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = CollectionSummarySelectionForm(instance=object, 
                                              initial={'last_used_collection': collection},
                                              data=request.POST,
                                              request=request)

        if form.is_valid():

            cd = form.cleaned_data

            collection = cd.get('last_used_collection')

            object.set_last_used_collection(collection)

            object.save()

            messages.success(request, 'EXISTING Bench ' + object.get_formatted_id() + ' Updated!')

    else:

        form = CollectionSummarySelectionForm(instance=object,
                                              request=request,
                                              initial={'last_used_collection': collection})

    return render(request, template_name, {'form': form,
                                           'object': object})
