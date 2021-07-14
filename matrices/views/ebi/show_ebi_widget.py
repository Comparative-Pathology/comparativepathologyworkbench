#!/usr/bin/python3
###!
# \file         views_ebi.py
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
# This file contains the show_ebi_widget view routine
#
###
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

from django.shortcuts import render

from matrices.models import Server

from matrices.routines import get_header_data

NO_CREDENTIALS = ''

#
# BROWSE THE EBI SERVER WIDGET
#
@login_required()
def show_ebi_widget(request, server_id, experiment_id):
    """
    Show the EBI widget
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_omero547() or server.is_omero56():

            server_data = server.get_ebi_widget_json()

            gene = ''

            data.update({ 'experimentAccession': experiment_id, 'geneId': gene })

            data.update(server_data)

            return render(request, 'ebi/show_widget.html', data)
