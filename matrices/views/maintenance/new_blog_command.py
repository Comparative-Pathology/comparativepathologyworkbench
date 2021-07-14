#!/usr/bin/python3
###!
# \file         views_maintenance.py
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
# This file contains the new_blog_command view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import BlogForm

from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# ADD A NEW COMMAND TO ACCESS THE BLOGGING ENGINE
#
@login_required
def new_blog_command(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = BlogForm(request.POST)

            if form.is_valid():

                blog = form.save(commit=False)

                blog.set_owner(request.user)

                blog.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = BlogForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_blog_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
