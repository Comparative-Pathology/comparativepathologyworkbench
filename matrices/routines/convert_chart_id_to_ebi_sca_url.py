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
    option = ''
    geneId = ''
    colourBy = ''
    type = ''

    chart_array = a_chart_id.split("_")

    datetime = chart_array[0]
    experiment_id = chart_array[1]
    type = chart_array[2]
    option = chart_array[3]
    colourBy = chart_array[4]
    geneId = chart_array[5]

    query_parameter_type = ''
    query_parameter_type = 'plotType=' + type.lower()

    query_parameter_option = ''
    query_parameter_option = '&plotOption=' + option

    query_parameter_colourBy = ''
    query_parameter_colourBy = '&colourBy=' + colourBy

    query_parameter_geneId = ''

    size = len(geneId)
    geneId_no_filetype = geneId[:size - 4]

    if geneId_no_filetype == 'NoGene':

        query_parameter_geneId = ''

    else:

        query_parameter_geneId = '&geneId=' + geneId_no_filetype

    query_parameter = query_parameter_type + query_parameter_option + query_parameter_colourBy + query_parameter_geneId

    #/json/experiments/
    ebi_sca_web = config('EBI_SCA_EXPERIMENTS_URL')

    path_array = ebi_sca_web.split("/")

    an_ebi_sca_url = 'https://' + a_url_server + '/' + path_array[1] + '/' + experiment_id + '/results/tsne?' + query_parameter

    return an_ebi_sca_url
