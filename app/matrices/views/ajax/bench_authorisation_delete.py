#!/usr/bin/python3
###!
# \file         bench_authorisation_delete.py
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
# This file contains the AJAX bench_authorisation_delete view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.models import Authorisation
from matrices.models import Matrix

from matrices.routines import credential_exists
from matrices.routines import exists_update_for_bench_and_user


#
# DELETE A BENCH AUTHORISATION
#
@login_required()
def bench_authorisation_delete(request, authorisation_id):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    authorisation = get_object_by_uuid_or_404(Authorisation, authorisation_id)
    bench = get_object_by_uuid_or_404(Matrix, authorisation.matrix.id)

    if not exists_update_for_bench_and_user(bench, request.user):

        raise PermissionDenied


    authorisation_id = authorisation.id

    authorisation.delete()

    return JsonResponse({'object_id': authorisation_id})
