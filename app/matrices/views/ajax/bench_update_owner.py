#!/usr/bin/python3
#
# ##
# \file         bench_update_owner.py
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
# This file contains the AJAX bench_update_owner view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

from matrices.forms import MatrixOwnerSelectionForm

from matrices.models import Authorisation
from matrices.models import Credential
from matrices.models import Matrix

from matrices.routines import authorisation_exists_for_bench_and_permitted
from matrices.routines import is_request_ajax


#
#   Re-Allocate the Bench Owner
#
@login_required()
def bench_update_owner(request, bench_id):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    bench = Matrix.objects.get_or_none(id=bench_id)

    if not bench:

        raise PermissionDenied

    old_owner = bench.owner

    if bench.is_locked():

        raise PermissionDenied

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = MatrixOwnerSelectionForm(instance=bench, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            new_owner = object.owner

            if not authorisation_exists_for_bench_and_permitted(bench, old_owner):

                bench_authorisation_old = Authorisation.objects.get(Q(matrix=bench) &
                                                                    Q(permitted=new_owner))

                bench_authorisation_new = Authorisation.create(bench,
                                                               old_owner,
                                                               bench_authorisation_old.authority)

                bench_authorisation_old.delete()
                bench_authorisation_new.save()

            object.save()

            messages.success(request, 'New Owner ' + str(object.owner.username) +
                             ' for Bench ' + bench.get_formatted_id() + ' Updated!')

    else:

        form = MatrixOwnerSelectionForm(instance=bench, initial={'owner': bench.owner.id}, )

    return render(request, template_name, {'form': form,
                                           'object': bench})
