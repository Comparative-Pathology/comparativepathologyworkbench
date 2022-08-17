#!/usr/bin/python3
###!
# \file         delete_bench_authority.py
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
# This file contains the delete_bench_authority view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Authority

from matrices.routines import exists_bench_authorisation_viewer
from matrices.routines import exists_bench_authorisation_editor

#
# DELETE A BENCH AUTHORITY
#
@login_required
def delete_bench_authority(request, bench_authority_id):

    if request.user.is_superuser:

        authority = get_object_or_404(Authority, pk=bench_authority_id)

        if authority.is_viewer() and exists_bench_authorisation_viewer():

            messages.error(request, 'CPW_WEB:0460 Bench Authority ' + authority.name + ' NOT Deleted - VIEWER Bench Authorisations still exist!')

        else:

            if authority.is_editor() and exists_bench_authorisation_editor():

                messages.error(request, 'CPW_WEB:0470 Bench Authority ' + authority.name + ' NOT Deleted - EDITOR Bench Authorisations still exist!')

            else:

                messages.success(request, 'Bench Authority ' + authority.name + ' Deleted!')
                authority.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
