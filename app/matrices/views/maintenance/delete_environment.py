#!/usr/bin/python3
#
# ##
# \file         delete_environment.py
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
# This file contains the delete_environment view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Environment


#
#   DELETE AN ENVIRONMENT
#
@login_required
def delete_environment(request, environment_id):

    if request.user.is_superuser:

        environment = Environment.objects.get_or_none(id=environment_id)

        if environment:

            if environment.name == 'CPW':

                messages.error(request, 'CPW_WEB:0510 Environment Location ' + environment.name + ' NOT Deleted - '
                               'CANNOT Delete the Primary Environment!')

            else:

                messages.success(request, 'Environment ' + environment.name + ' Deleted!')

                environment.delete()

            return HttpResponseRedirect(reverse('maintenance', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
