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
# This file contains the show_ebi_sca_server view routine
#
###
from __future__ import unicode_literals

import subprocess
from subprocess import call

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from decouple import config

from matrices.models import Server

from matrices.forms import SearchUrlForm

from matrices.routines import convert_url_ebi_sca_to_json
from matrices.routines import get_an_ebi_sca_experiment_id
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection
from matrices.routines import create_an_ebi_sca_chart
from matrices.routines import convert_url_ebi_sca_to_chart_id

HTTP_POST = 'POST'
NO_CREDENTIALS = ''

#
# SHOW A SEARCH BOX FOR AN EBI SERVER
#
@login_required()
def show_ebi_sca_server(request, server_id):
    """
    Show the EBI SCA Server
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_ebi_sca():

            form = SearchUrlForm()

            if request.method == HTTP_POST:

                form = SearchUrlForm(request.POST)

                if form.is_valid():

                    cd = form.cleaned_data

                    url_string = cd.get('url_string')

                    url_string_out = convert_url_ebi_sca_to_json(url_string)

                    if url_string_out == "":

                        messages.error(request, "URL not found!")
                        form.add_error(None, "URL not found!")

                    else:

                        temp_dir = config('HIGHCHARTS_TEMP_DIR')
                        output_dir = config('HIGHCHARTS_OUTPUT_DIR')
                        highcharts_host = config('HIGHCHARTS_HOST')
                        highcharts_web = config('HIGHCHARTS_OUTPUT_WEB')

                        experiment_id = get_an_ebi_sca_experiment_id(url_string)

                        chart_id = convert_url_ebi_sca_to_chart_id(url_string)

                        shell_command = create_an_ebi_sca_chart(url_string_out, experiment_id, chart_id, highcharts_host, temp_dir, output_dir)

                        success = call(str(shell_command), shell=True)

                        if success != 0:
                            print("shell_command : FAILED!")
                            print("shell_command : " + str(shell_command))

                        return redirect('webgallery_show_ebi_sca_image', server_id=server.id, image_id=chart_id)

                else:

                    messages.error(request, "ERROR: Form is Invalid!")
                    form.add_error(None, "ERROR: Form is Invalid!")

            else:

                form = SearchUrlForm()

            data.update({ 'server': server, 'form': form })

            return render(request, 'gallery/show_ebi_sca_server.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))
