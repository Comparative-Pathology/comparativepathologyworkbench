#!/usr/bin/python3
###!
# \file         convert_url_ebi_sca_to_json.py
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
# try to convert an EBI SCA URL to a CPW Equivalent?
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.db.models import Q

from django.apps import apps

from urllib.parse import urlparse

from matrices.routines import exists_server_for_url
from matrices.routines import get_server_list_for_url
from matrices.routines.validate_an_omero_url import validate_an_omero_url
from matrices.routines.validate_an_ebi_sca_url import validate_an_ebi_sca_url


"""
    Try to convert an EBI SCA URL to a CPW Equivalent?
"""
def convert_url_ebi_sca_to_json(a_url):

    url_string_out = ""

    if validate_an_ebi_sca_url(a_url):

        result = urlparse(a_url)

        if all([result.scheme, result.netloc, result.path, result.query]):

            path_array = result.path.split("/")

            url_out_prefix = result.scheme + '://' + result.netloc + '/' + path_array[1] + '/' + path_array[2] + '/json/cell-plots/'

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

            url_out_suffix = ''

            if type == 'tsne':

                url_out_suffix = '?plotMethod=tsne&perplexity=' + str(option)

            if type == 'umap':

                url_out_suffix = '?plotMethod=umap&n_neighbors=' + str(option)

            if geneId != '':

                url_string_out = url_out_prefix + experiment_id + '/expression/' + geneId + url_out_suffix

            else:

                if colourBy.isnumeric():

                    url_string_out = url_out_prefix + experiment_id + '/clusters/k/' + str(colourBy) + url_out_suffix

                else:

                    url_string_out = url_out_prefix + experiment_id + '/clusters/metadata/' + str(colourBy) + url_out_suffix

    return url_string_out
