#!/usr/bin/python3
#
# ##
# \file         delete_user.py
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
# This file contains the delete_user view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Authorisation
from matrices.models import Credential

from matrices.routines import get_or_none_user
from matrices.routines import exists_collection_authorisation_for_permitted
from matrices.routines import exists_bench_for_user
from matrices.routines import exists_collection_for_user
from matrices.routines import exists_image_for_user


#
#   DELETE A USER
#
@login_required
def delete_user(request, user_id):

    if request.user.is_superuser:

        subject = get_or_none_user(user_id)

        if not subject:

            messages.error(request, 'CPW_WEB:043 User NOT Deleted - User does NOT Exist!')

        else:

            authorisation = Authorisation.objects.get_or_none(permitted=subject)

            if authorisation:

                messages.error(request, 'CPW_WEB:0370 User NOT Deleted - Outstanding Bench Permissions Exist!')

            else:

                if exists_collection_authorisation_for_permitted(subject):

                    messages.error(request, 'CPW_WEB:0380 User NOT Deleted - Outstanding Collection Permissions Exist!')

                else:

                    if exists_bench_for_user(subject):

                        messages.error(request, 'CPW_WEB:0390 User NOT Deleted - Outstanding Benches Exist!')

                    else:

                        if exists_collection_for_user(subject):

                            messages.error(request, 'CPW_WEB:0400 User NOT Deleted - Outstanding Collections Exist!')

                        else:

                            if exists_image_for_user(subject):

                                messages.error(request, 'CPW_WEB:0410 User NOT Deleted - Outstanding Images Exist!')

                            else:

                                credential = Credential.objects.get_or_none(username=subject.username)

                                if credential:

                                    messages.error(request, 'CPW_WEB:0420 User NOT Deleted - Outstanding Blog Credential '
                                                   'Exists!')

                                else:

                                    messages.success(request, 'User ' + subject.username + ' Deleted!')
                                subject.delete()

            return HttpResponseRedirect(reverse('authorisation', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
