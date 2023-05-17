#!/usr/bin/python3
###!
# \file         show_ebi_sca_upload_server.py
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
# This file contains the show_ebi_sca_upload_server view routine
#
###
from __future__ import unicode_literals

import os
import subprocess
from subprocess import call

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Server

from matrices.models import Document

from matrices.forms import DocumentForm

from matrices.routines import credential_exists
from matrices.routines import convert_url_ebi_sca_to_json
from matrices.routines import get_an_ebi_sca_experiment_id
from matrices.routines import get_header_data
from matrices.routines import convert_url_ebi_sca_to_chart_id
from matrices.routines import validate_an_ebi_sca_image
from matrices.routines import validate_an_ebi_sca_url


HTTP_POST = 'POST'


#
# SHOW A SEARCH BOX FOR AN EBI SERVER TO UPLOAD A FILE
#
@login_required()
def show_ebi_sca_upload_server(request, server_id):
    """
    Show the EBI SCA Server
    """

    if request.user.username == 'guest':

        raise PermissionDenied


    data = get_header_data(request.user)

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=server_id)

        if server.is_ebi_sca():

            if request.method == HTTP_POST:

                form = DocumentForm(request.POST, request.FILES)

                if form.is_valid():

                    cd = form.cleaned_data

                    url_string = cd.get('source_url')

                    if validate_an_ebi_sca_url(url_string):

                        url_string_out = convert_url_ebi_sca_to_json(url_string)

                        if url_string_out == "":

                            messages.error(request, "CPW_WEB:0040 Show EBI SCA - URL not found!")
                            form.add_error(None, "CPW_WEB:0040 Show EBI SCA - URL not found!")

                        else:

                            if Document.objects.filter(owner=request.user).exists():

                                Document.objects.filter(owner=request.user).delete()

                            experiment_id = get_an_ebi_sca_experiment_id(url_string)

                            chart_id = convert_url_ebi_sca_to_chart_id(url_string)

                            document = form.save(commit=False)

                            document.set_owner(request.user)

                            upload_chart = str(document.location)

                            if validate_an_ebi_sca_image(upload_chart):

                                document.save()

                                initial_path = document.location.path

                                new_chart_id = '/' + chart_id

                                new_path = str(settings.MEDIA_ROOT) + new_chart_id

                                document.set_location(new_chart_id)

                                os.rename(initial_path, new_path)

                                document.save()

                                return redirect('webgallery_show_ebi_sca_image', server_id=server.id, image_id=chart_id)

                            else:

                                messages.error(request, "CPW_WEB:0250 Show CPW Upload - Invalid Image Type!")
                                form.add_error(None, "CPW_WEB:0250 Show CPW Upload - Invalid Image Type!")

                    else:

                        messages.error(request, "CPW_WEB:0210 Show CPW Upload - Invalid EBI SCA URL!")
                        form.add_error(None, "CPW_WEB:0210 Show CPW Upload - Invalid EBI SCA URL!")

                else:

                    messages.error(request, "CPW_WEB:0060 Show EBI SCA Upload - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0060 Show EBI SCA Upload - Form is Invalid!")

            else:

                form = DocumentForm()

            data.update({ 'server': server, 'form': form })

            return render(request, 'gallery/show_ebi_sca_upload_server.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
