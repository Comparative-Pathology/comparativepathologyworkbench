#!/usr/bin/python3
#
# ##
# \file         authorisation_crud_consequences.py
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
# Consequential Actions for Bench Authorisation Updates
# ##
#
from __future__ import unicode_literals

from django.db.models import Q

from django.apps import apps

from matrices.routines.authorisation_exists_for_bench_and_permitted import authorisation_exists_for_bench_and_permitted


#
#   Consequential Actions for Bench Authorisation Updates
#
def authorisation_crud_consequences(a_permitted, a_matrix, a_authority):

    Authorisation = apps.get_model('matrices', 'Authorisation')

    if authorisation_exists_for_bench_and_permitted(a_matrix, a_permitted):

        authorisation_old = Authorisation.objects.get(Q(matrix=a_matrix) & Q(permitted=a_permitted))

        authorisation_old.delete()
