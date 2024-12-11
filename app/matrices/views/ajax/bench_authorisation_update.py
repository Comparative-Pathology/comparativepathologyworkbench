#!/usr/bin/python3
#
# ##
# \file         bench_authorisation_update.py
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
# This file contains the AJAX authorisation_update view routine
# ##
#
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.forms import AuthorisationForm

from matrices.models import Matrix
from matrices.models import Authorisation
from matrices.models import Authority
from matrices.models import Credential

from matrices.routines import authorisation_crud_consequences
from matrices.routines import exists_update_for_bench_and_user


#
#   EDIT A BENCH AUTHORISATION
#
@login_required()
def bench_authorisation_update(request, authorisation_id, bench_id=None):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    object = Authorisation.objects.get_or_none(id=authorisation_id)

    if not object:

        raise PermissionDenied

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = AuthorisationForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            permitted = form.cleaned_data['permitted']
            bench = form.cleaned_data['bench']
            authority = form.cleaned_data['authority']

            if not exists_update_for_bench_and_user(bench, request.user):

                raise PermissionDenied

            object.set_matrix(bench)
            object.set_authority(authority)

            authorisation_crud_consequences(permitted, bench, authority)

            object.save()

            messages.success(request, 'Authorisation ' + str(object.id) + ' UPDATED for Bench ' +
                             object.matrix.get_formatted_id())

    else:

        form = AuthorisationForm(instance=object)

    if bench_id is None:

        if request.user.is_superuser:

            form.fields['bench'] = forms.ModelChoiceField(Matrix.objects.all())

        else:

            form.fields['bench'] = forms.ModelChoiceField(Matrix.objects.filter(owner=request.user))

    else:

        bench = Matrix.objects.get_or_none(id=bench_id)

        if not bench:

            raise PermissionDenied

        if not exists_update_for_bench_and_user(bench, request.user):

            raise PermissionDenied

        form.fields['bench'] = forms.ModelChoiceField(Matrix.objects.filter(id=bench_id))
        form.fields['bench'].initial = bench_id

    form.fields['authority'] = forms.ModelChoiceField(Authority.objects.all())
    form.fields['authority'].initial = object.authority.id
    form.fields['authority'].label_from_instance = lambda obj: "{0}".format(obj.name)

    form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
    form.fields['permitted'].initial = object.permitted.id
    form.fields['permitted'].label_from_instance = lambda obj: "{0}".format(obj.username)

    form.fields['bench'].label_from_instance = lambda obj: "CPW:{0:06d}, {1}".format(obj.id, obj.title)

    return render(request, template_name, {'form': form,
                                           'object': object})
