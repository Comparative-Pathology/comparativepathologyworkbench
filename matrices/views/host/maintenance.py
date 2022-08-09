#!/usr/bin/python3
###!
# \file         maintenance.py
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
# This file contains the maintenance view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Command
from matrices.models import Blog
from matrices.models import Authority
from matrices.models import CollectionAuthority

from matrices.routines import get_header_data

#
# SHOW THE MAINTENANCE PAGE
#
@login_required
def maintenance(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        type_list = Type.objects.all()
        protocol_list = Protocol.objects.all()
        command_list = Command.objects.all()
        blog_list = Blog.objects.all()
        authority_list = Authority.objects.all()
        collection_authority_list = CollectionAuthority.objects.all()

        data.update({ 'type_list': type_list, 'protocol_list': protocol_list, 'command_list': command_list, 'blog_list': blog_list, 'authority_list': authority_list, 'collection_authority_list': collection_authority_list })

        return render(request, 'host/maintenance.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
