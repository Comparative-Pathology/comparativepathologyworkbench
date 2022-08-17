#!/usr/bin/python3
###!
# \file         delete_type.py
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
# This file contains the delete_type view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Type

from matrices.routines import exists_server_for_type
from matrices.routines import exists_command_for_type
from matrices.routines import exists_blog_command_for_type

#
# DELETE A TYPE OF SERVER
#
@login_required
def delete_type(request, type_id):

    if request.user.is_superuser:

        type = get_object_or_404(Type, pk=type_id)

        if exists_server_for_type(type):

            messages.error(request, 'CPW_WEB:0510 Server Type ' + type.name + ' NOT Deleted - Servers still exist!')

        else:

            if exists_command_for_type(type):

                messages.error(request, 'CPW_WEB:0520 Server Type ' + type.name + ' NOT Deleted - API Commands still exist!')

            else:

                messages.success(request, 'Server Type ' + type.name + ' Deleted!')

                type.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
