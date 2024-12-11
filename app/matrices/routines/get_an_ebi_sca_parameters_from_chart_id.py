#!/usr/bin/python3
#
# ##
# \file         get_an_ebi_sca_parameters_from_chart_id.py
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
# Extract the EBI SCA Experiment Id from a Chart Id
# ##
#
from __future__ import unicode_literals

from matrices.routines.convert_chart_id_to_ebi_sca_url import convert_chart_id_to_ebi_sca_url
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment


#
#   Extract the EBI SCA Experiment Id from an EBI SCA URL
#
def get_an_ebi_sca_parameters_from_chart_id(a_url_server, a_chart_id):

    environment = get_primary_cpw_environment()

    highcharts_web = environment.get_full_web_root()

    chart_key = ''
    experiment_id = ''
    type = ''
    option = ''
    geneId = ''
    colourBy = ''
    geneId = ''

    birdseye_url = highcharts_web + '/' + a_chart_id
    viewer_url = convert_chart_id_to_ebi_sca_url(a_url_server, a_chart_id)

    chart_array = a_chart_id.split("_")

    datetime = chart_array[0]
    new_datetime = datetime.replace('-', '').replace(':', '').replace('.', '')

    size = len(new_datetime)
    chart_key = new_datetime[8:size + 9]

    experiment_id = chart_array[1]
    type = chart_array[2]
    option = chart_array[3]
    colourBy = chart_array[4]

    fifth_parameter_suffix = chart_array[5]

    size = len(fifth_parameter_suffix)
    fifth_parameter = fifth_parameter_suffix[:size - 4]

    if fifth_parameter == "NoGene":

        geneId = ''

    else:

        prefix = fifth_parameter[0:4]

        if prefix == 'ENSG':

            geneId = fifth_parameter

        else:

            geneId = ''

    chart_parameters = ({
        'chart_key': chart_key,
        'experiment_id': experiment_id,
        'chart_id': a_chart_id,
        'viewer_url': viewer_url,
        'birdseye_url': birdseye_url,
        'type': type,
        'option': option,
        'geneId': geneId,
        'colourBy': colourBy
    })

    return chart_parameters
