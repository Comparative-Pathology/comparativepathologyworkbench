#!/usr/bin/python3
###!
# \file         views_permissions.py
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
# This file contains the edit_bench_authorisation view routine
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matrices.forms import AuthorisationForm

from matrices.models import Authorisation
from matrices.models import Matrix

from matrices.routines import authorisation_exists_for_bench_and_permitted
from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# CREATE A BENCH AUTHORISATION
#
@login_required
def edit_bench_authorisation(request, bench_authorisation_id):

    data = get_header_data(request.user)

    authorisation = get_object_or_404(Authorisation, pk=bench_authorisation_id)

    if request.method == HTTP_POST:

        next_page = request.POST.get('next', '/')

        form = AuthorisationForm(request.POST, instance=authorisation)

        if form.is_valid():

            authorisation = form.save(commit=False)

            if authorisation_exists_for_bench_and_permitted(authorisation.matrix, authorisation.permitted):

                authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))

                if authorisation_old.authority != authorisation.authority:

                    authorisation_old.authority = authorisation.authority

                    authorisation_old.save()

            else:

                authorisation.save()

            return HttpResponseRedirect(next_page)

        else:

            text_flag = ''

            messages.error(request, "Bench Authorisation Form is Invalid!")
            form.add_error(None, "Bench Authorisation Form is Invalid!")

            data.update({ 'text_flag': text_flag, 'form': form, 'authorisation': authorisation })

    else:

        text_flag = ''

        form = AuthorisationForm(instance=authorisation)

        if request.user.is_superuser:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.all())

        else:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(owner=request.user))

        form.fields['matrix'].initial = authorisation.matrix.id

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form, 'authorisation': authorisation })

    return render(request, 'permissions/edit_bench_authorisation.html', data)
