#!/usr/bin/python3
###!
# \file         views_gallery.py
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
# This file contains the add_image view routine
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

from matrices.models import Server

from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import add_image_to_collection

NO_CREDENTIALS = ''

#
# ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
@login_required
def add_image(request, server_id, image_id, roi_id):

    data = get_header_data(request.user)

    if not exists_active_collection_for_user(request.user):

        return HttpResponseRedirect(reverse('home', args=()))


    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if exists_active_collection_for_user(request.user):

            image = add_image_to_collection(request.user, server, image_id, roi_id)

        else:

            messages.error(request, "You have no Active Image Collection; Please create a Collection!")

        if server.is_omero547() or server.is_omero56():

            return HttpResponseRedirect(reverse('webgallery_show_image', args=(server_id, image_id)))

        else:

            if server.is_wordpress():

                return HttpResponseRedirect(reverse('webgallery_show_wordpress_image', args=(server_id, image_id)))
