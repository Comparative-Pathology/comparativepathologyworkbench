#!/usr/bin/python3
#
# ##
# \file         exists_update_for_bench_and_user.py
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
# Can the supplied User UPDATE the supplied Bench?
# ##
#
from __future__ import unicode_literals

from django.apps import apps

from django.db.models import Q


#
#   Get the Authorisation for a particular Bench and particular User
#
def exists_update_for_bench_and_user(a_matrix, a_user):

    Authorisation = apps.get_model('matrices', 'Authorisation')

    update_authority = False

    if a_user.is_superuser:

        update_authority = True

    else:

        if a_user == a_matrix.owner:

            update_authority = True

        else:

            if Authorisation.objects.filter(Q(matrix=a_matrix) & Q(permitted=a_user)).exists():

                authorisation = Authorisation.objects.get(Q(matrix=a_matrix) & Q(permitted=a_user))

                if authorisation.authority.is_owner():

                    update_authority = True

                if authorisation.authority.is_admin():

                    update_authority = True

                if authorisation.authority.is_viewer():

                    update_authority = False

                if authorisation.authority.is_editor():

                    update_authority = True

            else:

                update_authority = False

    return update_authority
