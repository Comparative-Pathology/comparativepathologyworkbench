#!/usr/bin/python3
###!
# \file         bench_authorisation_create.py
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
# This file contains the AJAX bench_authorisation_create view routine
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

from matrices.forms import AuthorisationForm

from matrices.models import Matrix
from matrices.models import Authority
from matrices.models import Authorisation

from matrices.routines import authorisation_crud_consequences
from matrices.routines import credential_exists
from matrices.routines import exists_update_for_bench_and_user
from matrices.routines import simulate_network_latency


#
# ADD A BENCH AUTHORISATION
#
@login_required()
def bench_authorisation_create(request, bench_id=None):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    object = None

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = AuthorisationForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            permitted = form.cleaned_data['permitted']
            bench = form.cleaned_data['matrix']
            authority = form.cleaned_data['authority']

            if not exists_update_for_bench_and_user(bench, request.user):

                raise PermissionDenied


            object.set_authority(authority)

            authorisation_crud_consequences(permitted, bench, authority)

            object.save()

            messages.success(request, 'Bench Authorisation ' + str(object.id) + ' ADDED for Bench CPW:' + '{num:06d}'.format(num=object.matrix.id))

    else:

        form = AuthorisationForm()


    if bench_id is None:

        if request.user.is_superuser:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.all())

        else:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(owner=request.user))

    else:

        bench = get_object_by_uuid_or_404(Matrix, bench_id)

        if not exists_update_for_bench_and_user(bench, request.user):

            raise PermissionDenied


        form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(id=bench_id))
        form.fields['matrix'].initial = bench_id

    form.fields['authority'] = forms.ModelChoiceField(Authority.objects.all())

    form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))


    return render(request, template_name, {
        'form': form,
        'object': object
    })
