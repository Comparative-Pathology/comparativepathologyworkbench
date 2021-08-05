#!/usr/bin/python3
###!
# \file         exists_server_for_uid_url.py
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
# Convert a CPW Chart Id to an EBI SCA URL
###
from __future__ import unicode_literals

import base64, hashlib

from datetime import datetime

from os import urandom

from decouple import config

"""
    Convert a CPW Chart Id to an EBI SCA URL
"""
def convert_chart_id_to_ebi_sca_url(a_url_server, a_chart_id):

    experiment_id = ''
    perplexity = ''
    k_value = ''
    geneId = ''
    colourBy = ''
    metadata = ''

    chart_array = a_chart_id.split("_")

    datetime = chart_array[0]
    experiment_id = chart_array[1]
    perplexity = chart_array[2]
    third_parameter_suffix = chart_array[3]

    size = len(third_parameter_suffix)
    third_parameter = third_parameter_suffix[:size - 4]

    query_parameter = ''
    query_parameter = 'perplexity=' + perplexity

    if third_parameter.isnumeric():

        k_value = third_parameter
        query_parameter = query_parameter + '&colourBy=clusters&k=' + k_value

    else:

        prefix = third_parameter[0:4]

        if prefix == 'ENSG':

            geneId = third_parameter
            query_parameter = query_parameter + '&colourBy=clusters&geneId=' + geneId

        else:

            chart_prefix = datetime + '_' + experiment_id + '_' + perplexity + '_'
            size_prefix = len(chart_prefix)
            size_chart_id = len(a_chart_id)
            metadata = a_chart_id[size_prefix: size_chart_id - 4]

            query_parameter = query_parameter + '&colourBy=metadata&metadata=' + metadata

    #/json/experiments/
    ebi_sca_web = config('EBI_SCA_EXPERIMENTS_URL')

    path_array = ebi_sca_web.split("/")

    an_ebi_sca_url = 'https://' + a_url_server + '/' + path_array[1] + '/' + experiment_id + '/results/tsne?' + query_parameter

    return an_ebi_sca_url
