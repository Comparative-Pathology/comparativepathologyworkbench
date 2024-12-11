#!/usr/bin/python3
#
# ##
# \file         publicise_bench.py
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
# This file contains the publicise_bench view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Credential
from matrices.models import Matrix


#
#   Publicise a Bench
#
@login_required
def publicise_bench(request, bench_id):

    bench = Matrix.objects.get_or_none(id=bench_id)

    if not bench:

        raise PermissionDenied

    if bench.is_locked():

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        bench.set_public()

        bench.save()

        messages.success(request, 'Bench ' + bench.get_formatted_id() + ' set PUBLIC!')

        return HttpResponseRedirect(reverse('list_benches', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
