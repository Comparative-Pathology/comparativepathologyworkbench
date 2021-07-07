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
# This file contains the view_collection_authority view routine
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

from matrices.forms import CommandForm
from matrices.forms import BlogForm
from matrices.forms import ProtocolForm
from matrices.forms import TypeForm
from matrices.forms import AuthorityForm
from matrices.forms import CollectionAuthorityForm

from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Command
from matrices.models import Blog
from matrices.models import Authority
from matrices.models import CollectionAuthority

from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# VIEW A COLLECTION AUTHORITY
#
@login_required
def view_collection_authority(request, collection_authority_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        collection_authority = get_object_or_404(CollectionAuthority, pk=collection_authority_id)

        data.update({ 'collection_authority_id': collection_authority_id, 'collection_authority': collection_authority })

        return render(request, 'maintenance/detail_collection_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
