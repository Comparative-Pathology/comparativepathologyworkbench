#!/usr/bin/python3
###!
# \file         views_authorisation.py
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
# This file contains the collectivization view routine
#
###
from __future__ import unicode_literals

import os
import time
import requests

from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Q

from decouple import config

from matrices.forms import CredentialForm
from matrices.forms import EditUserForm

from matrices.models import Credential
from matrices.models import Collection

from matrices.routines import exists_image_for_user
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_images_for_user
from matrices.routines import credential_exists
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# SETUP DEFAULT COLLECTIONS VIEW
#
def collectivization(request):

    data = get_header_data(request.user)

    if request.user.is_superuser:

        user_list = User.objects.all()

        out_message_list = list()

        for user in user_list:

            imageCount = 0

            out_message = ""

            if exists_image_for_user(user):

                image_list = get_images_for_user(user)

                if exists_active_collection_for_user(user):

                    out_message = "Default Collection ALREADY exists for User {}".format( user.username )

                else:

                    collection = Collection.create("Default Collection", "Default Collection", True, user)

                    collection.save()

                    for image in image_list:

                        imageCount = imageCount + 1

                        Collection.assign_image(image, collection)

                    out_message = "Default Collection created for {} Images for User {}".format( imageCount, user.username )

            else:

                out_message = "NO Default Collection created for User {}".format( user.username )

            out_message_list.append(out_message)

        data.update({ 'out_message_list': out_message_list })

        return render(request, 'authorisation/collectivization.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
