#!/usr/bin/python3
###!
# \file         signup.py
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
# This file contains the signup view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from matrices.forms import SignUpForm

from matrices.routines import get_header_data

from matrices.tokens import account_activation_token

HTTP_POST = 'POST'


#
#   VIEWS FOR SIGNUP
#
def signup(request):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.is_active = False

            user.save()

            current_site = get_current_site(request)

            subject = 'Activate Your Comparative Pathology Workbench Account'

            message = render_to_string('user/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)

            return redirect('account_activation_sent')

        else:

            messages.error(request, "CPW_WEB:0360 Sign Up - Form is Invalid!")
            form.add_error(None, "CPW_WEB:0360 Sign Up - Form is Invalid!")

            data.update({'form': form})

    else:

        form = SignUpForm()

        data.update({'form': form})

    return render(request, 'user/signup.html', data)
