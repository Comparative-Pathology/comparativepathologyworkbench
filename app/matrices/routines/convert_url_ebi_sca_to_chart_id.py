#!/usr/bin/python3
###!
# \file         convert_url_ebi_sca_to_chart_id.py
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
# Convert an EBI SCA URL to a CPW Chart Id
###
from __future__ import unicode_literals

import base64, hashlib

from datetime import datetime

from os import urandom

from urllib.parse import urlparse

from matrices.routines import exists_server_for_url
from matrices.routines import get_server_list_for_url
from matrices.routines.validate_an_omero_url import validate_an_omero_url
from matrices.routines.validate_an_ebi_sca_url import validate_an_ebi_sca_url


"""
    Convert an EBI SCA URL to a CPW Chart Id
"""
def convert_url_ebi_sca_to_chart_id(a_url):

    chart_string_out = ""

    if validate_an_ebi_sca_url(a_url):

        result = urlparse(a_url)

        if all([result.scheme, result.netloc, result.path, result.query]):

            path_array = result.path.split("/")

            experiment_id = path_array[4]

            query_array = result.query.split("&")

            option = ''
            type = ''
            geneId = ''
            colourBy = ''

            for array_entry in query_array:

                array_entry_array = array_entry.split("=")
                prefix = array_entry_array[0]
                suffix = array_entry_array[1]

                if prefix == 'plotOption':

                    option = suffix

                if prefix == 'plotType':

                    type = suffix

                if prefix == 'geneId':

                    geneId = suffix

                if prefix == 'colourBy':

                    colourBy = suffix

            now = datetime.now()
            date_time = now.strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

            if geneId != '':

                chart_string_out = date_time + '_' + experiment_id + '_' + str(type.upper()) + '_' + str(option) + '_' + str(colourBy) + '_' + geneId + '.png'

            else:

                chart_string_out = date_time + '_' + experiment_id + '_' + str(type.upper()) + '_' + str(option) + '_' + str(colourBy) + '_NoGene' + '.png'

    return chart_string_out
