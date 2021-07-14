#!/usr/bin/python3
###!
# \file         views_user.py
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
# This file contains activate view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse

from matrices.tokens import account_activation_token

#
# ACCOUNT ACTIVATE
#
def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):

        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        return render(request, 'user/account_activation_invalid.html')
