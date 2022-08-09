#!/usr/bin/python3
###!
# \file         collection_read.py
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
# This file contains the AJAX collection_read.py view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.models import Collection


#
# READ A COLLECTION AUTHORISATION
#
@login_required()
def collection_read(request, collection_id):

    object = get_object_by_uuid_or_404(Collection, collection_id)

    htmlString = '<dl class=\"standard\">'\
		'<dt>Title</dt>'\
		'<dd>' + object.title + '</dd>'\
		'<dt>Description</dt>'\
		'<dd>' + object.description + '</dd>'\
		'<dt>Owner</dt>'\
		'<dd>' + object.owner.username + '</dd>'\
		'<dt>Active</dt>'\
		'<dd>' + str(object.active) + '</dd>'\
	'</dl>'

    return HttpResponse(htmlString)
