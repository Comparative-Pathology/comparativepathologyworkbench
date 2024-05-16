#!/usr/bin/python3
###!
# \file         privatise_bench.py
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
# This file contains the privatise_bench view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Matrix

from matrices.routines import credential_exists


#
#   Privatise a Bench
#
@login_required
def privatise_bench(request, bench_id):

    if credential_exists(request.user):

        bench = get_object_or_404(Matrix, pk=bench_id)

        bench.set_private()

        bench.save()

        matrix_id_formatted = "CPW:" + "{:06d}".format(bench.id)
        messages.success(request, 'Bench ' + matrix_id_formatted + ' set PRIVATE!')

        return HttpResponseRedirect(reverse('list_benches', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
