#!/usr/bin/python3
###!
# \file         edit_bench_authority.py
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
# This file contains the edit_bench_authority view routine
#
###
from __future__ import unicode_literals

import time

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import AuthorityForm

from matrices.models import Authority

from matrices.routines import get_header_data

HTTP_POST = 'POST'


#
#   EDIT A BENCH AUTHORITY
#
@login_required
def edit_bench_authority(request, bench_authority_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        authority = get_object_or_404(Authority, pk=bench_authority_id)

        if request.method == HTTP_POST:

            time.sleep(3.0)

            form = AuthorityForm(request.POST, instance=authority)

            if form.is_valid():

                authority = form.save(commit=False)

                authority.set_owner(request.user)

                authority.save()

                messages.success(request, 'Bench Authority ' + authority.name + ' Updated!')

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "CPW_WEB:0090 Edit Bench Authority - Form is Invalid!")
                form.add_error(None, "CPW_WEB:0090 Edit Bench Authority - Form is Invalid!")

                data.update({ 'form': form, 'authority': authority })

        else:

            form = AuthorityForm(instance=authority)

            data.update({ 'form': form, 'authority': authority })

        return render(request, 'maintenance/edit_bench_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
