#!/usr/bin/python3
###!
# \file         show_cpw_upload_server.py
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
# This file contains the show_cpw_upload_server view routine
#
###
from __future__ import unicode_literals

import os

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from decouple import config

from matrices.models import Server

from matrices.models import Document

from matrices.forms import DocumentForm

from matrices.routines import credential_exists
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection
from matrices.routines import validate_a_cpw_image
from matrices.routines import validate_a_cpw_url

HTTP_POST = 'POST'


#
# SHOW A SEARCH BOX FOR THE CPW SERVER TO UPLOAD A FILE
#
@login_required()
def show_cpw_upload_server(request, server_id):
    """
    Show the CPW Server
    """

    data = get_header_data(request.user)

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=server_id)

        if server.is_cpw():

            if request.method == HTTP_POST:

                form = DocumentForm(request.POST, request.FILES)

                if form.is_valid():

                    cd = form.cleaned_data

                    url_string = cd.get('source_url')

                    if validate_a_cpw_url(url_string):

                        if Document.objects.filter(owner=request.user).exists():

                            Document.objects.filter(owner=request.user).delete()

                        document = form.save(commit=False)

                        document.set_owner(request.user)

                        chart_id = str(document.location)

                        if validate_a_cpw_image(chart_id):

                            document.save()

                            now = datetime.now()
                            date_time = now.strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

                            initial_path = document.location.path
                            new_chart_id = date_time + '_' + chart_id
                            new_path = '/' + new_chart_id

                            new_full_path = settings.MEDIA_ROOT + new_path

                            document.set_location(new_path)

                            os.rename(initial_path, new_full_path)

                            document.save()

                            return redirect('webgallery_show_cpw_image', server_id=server.id, image_id=new_chart_id)

                        else:

                            messages.error(request, "CPW_WEB:00240 Show CPW Upload - Invalid Image Type!")
                            form.add_error(None, "CPW_WEB:0240 Show CPW Upload - Invalid Image Type!")

                    else:

                        messages.error(request, "CPW_WEB:0280 Show CPW Upload - Invalid URL!")
                        form.add_error(None, "CPW_WEB:0280 Show CPW Upload - Invalid URL!")

                else:

                    messages.error(request, "CPW_WEB:0080 Show CPW Upload - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0080 Show CPW Upload - Form is Invalid!")

            else:

                form = DocumentForm()

            data.update({ 'server': server, 'form': form })

            return render(request, 'gallery/show_cpw_upload_server.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
