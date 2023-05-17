#!/usr/bin/python3
###!
# \file         mailer.py
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
# This file contains the mailer view routine
#
###
from __future__ import unicode_literals

from django.core.mail import send_mail
from django.utils import timezone

from django.shortcuts import render

from matrices.routines import get_header_data
from matrices.routines import get_primary_cpw_environment

#
# MAILER VIEW
#
def mailer(request):

    data = get_header_data(request.user)

    environment  = get_primary_cpw_environment()

    if request.user.is_superuser:

        now = timezone.now()

        subject = 'A Time Check'
        message = 'Here is the time : ' + str(now)
        email_from = environment.from_email
        recipient_list = ['mike.wicks@gmail.com',]
        email_to = 'mike.wicks@gmail.com'

        data.update({ 'subject': subject, 'message': message, 'email_from': email_from, 'email_to': email_to })

        send_mail( subject, message, email_from, recipient_list, fail_silently=False )

    return render(request, 'authorisation/mailer.html', data)
