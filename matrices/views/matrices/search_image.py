#!/usr/bin/python3
###!
# \file         search_image.py
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
# This file contains the search_image view routine
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

from matrices.forms import SearchUrlForm

from matrices.models import Collection

from matrices.routines import credential_exists
from matrices.routines import convert_url_ebi_sca_to_chart_id
from matrices.routines import convert_url_ebi_sca_to_json
from matrices.routines import convert_url_omero_to_cpw
from matrices.routines import create_an_ebi_sca_chart
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_an_ebi_sca_experiment_id
from matrices.routines import get_header_data
from matrices.routines import get_images_for_collection
from matrices.routines import get_server_from_ebi_sca_url

HTTP_POST = 'POST'
LIST_IMAGING_HOSTS = "list_imaging_hosts"
VIEW_ACTIVE_COLLECTION = "view_active_collection"
VIEW_ALL_COLLECTIONS = "view_all_collections"
VIEW_COLLECTION = "view_collection"


#
# Search for an Image
#
@login_required
def search_image(request, path_from, identifier):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        form = SearchUrlForm()

        if request.method == HTTP_POST:

            form = SearchUrlForm(request.POST)

            if form.is_valid():

                cd = form.cleaned_data

                url_string = cd.get('url_string')

                url_string_ebi_sca_out = convert_url_ebi_sca_to_json(url_string)
                url_string_omero_out = convert_url_omero_to_cpw(request, url_string)

                if url_string_omero_out != '' and url_string_ebi_sca_out != '':

                    messages.error(request, "CPW_WEB:0410 Search Image - URL not found!")
                    form.add_error(None, "CPW_WEB:0410 Search Image - URL not found!")

                if url_string_omero_out == '' and url_string_ebi_sca_out == '':

                    messages.error(request, "CPW_WEB:0420 Search Image - URL not found!")
                    form.add_error(None, "CPW_WEB:0420 Search Image - URL not found!")

                if url_string_omero_out != '' and url_string_ebi_sca_out == '':

                    return redirect(url_string_omero_out)

                if url_string_omero_out == '' and url_string_ebi_sca_out != '':

                    messages.error(request, "CPW_WEB:0050 Search Image - URL not found!")
                    form.add_error(None, "CPW_WEB:0050 Search Image - URL not found!")

            else:

                messages.error(request, "CPW_WEB:0440 Search Image - Form is Invalid!")
                form.add_error(None, "CPW_WEB:0440 Search Image - Form is Invalid!")

        else:

            form = SearchUrlForm()

        return_page = ''

        if path_from == LIST_IMAGING_HOSTS:

            data.update({ 'form': form, 'search_from': "list_imaging_hosts" })

            return_page = 'host/list_imaging_hosts.html'


        if path_from == VIEW_ACTIVE_COLLECTION:

            collection_list = get_active_collection_for_user(request.user)
            collection = collection_list[0]
            collection_image_list = get_images_for_collection(collection)

            data.update({ 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_active_collection" })

            return_page = 'matrices/view_collection.html'


        if path_from == VIEW_ALL_COLLECTIONS:

            data.update({ 'form': form, 'search_from': "view_all_collections" })

            return_page = 'matrices/view_all_collections.html'


        if path_from == VIEW_COLLECTION:

            collection = get_object_or_404(Collection, pk=identifier)
            collection_image_list = get_images_for_collection(collection)

            data.update({ 'collection': collection, 'collection_image_list': collection_image_list, 'form': form, 'search_from': "view_collection" })

            return_page = 'matrices/view_collection.html'


        return render(request, return_page, data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
