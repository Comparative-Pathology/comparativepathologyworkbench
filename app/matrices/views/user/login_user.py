#!/usr/bin/python3
###!
# \file         login_user.py
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
# This file contains the login view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect

from django.shortcuts import redirect, render, reverse

from django.contrib.auth.forms import AuthenticationForm

from matrices.routines import get_header_data


HTTP_POST = 'POST'

#
# VIEW FOR LOGIN
#
def login_user(request):

    data = get_header_data(request.user)

    next = ""

    if request.GET:

        next = request.GET['next']

    if request.POST:

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
			
            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)

                if next == "":
        
                    return redirect(reverse('home', args=()))
                
                else:
                    
                    return HttpResponseRedirect(next)
        
        else:

            data.update({ 'form': form })

    else:

        form = AuthenticationForm()

        data.update({ 'form': form })
    
    return render(request, 'user/login.html', data)
