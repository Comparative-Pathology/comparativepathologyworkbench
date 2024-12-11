#!/usr/bin/python3
#
# ##
# \file         authorisationform.py
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
# Form for adding/editing Bench Authorisations.
# ##
#
from __future__ import unicode_literals

from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from matrices.models import Matrix
from matrices.models import Authority
from matrices.models import Authorisation

from matrices.routines import authorisation_exists_for_bench_and_permitted


#
#   BENCH AUTHORISATION FORM
#
class AuthorisationForm(forms.ModelForm):

    bench = forms.ModelChoiceField(queryset=Matrix.objects.all(), label=_('Bench'))
    permitted = forms.ModelChoiceField(queryset=User.objects.all())
    authority = forms.ModelChoiceField(queryset=Authority.objects.all())

    class Meta:
        model = Authorisation
        fields = ('bench', 'permitted', 'authority', )

    def clean(self):

        cleaned_data = super().clean()

        bench = cleaned_data.get("bench")
        permitted = cleaned_data.get("permitted")
        authority = cleaned_data.get("authority")

        if not bench:
            msg = "Please Select a Bench!"
            raise ValidationError(msg)

        if not permitted:
            msg = "Please Select a User to be Permitted!"
            raise ValidationError(msg)

        if not authority:
            msg = "Please Select an Authority!"
            raise ValidationError(msg)

        if authorisation_exists_for_bench_and_permitted(bench, permitted):

            authorisation_old = Authorisation.objects.get(Q(matrix=bench) & Q(permitted=permitted))

            if authorisation_old.authority == authority:

                msg = 'A Bench Authorisation for \"' + str(permitted.username) + '\" and ' + str(authority.name) +\
                    ' already exists for Bench ' + bench.get_formatted_id()
                raise ValidationError(msg)
