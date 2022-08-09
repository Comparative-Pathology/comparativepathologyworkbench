#!/usr/bin/python3
###!
# \file         create_an_ebi_sca_chart.py
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
# Create an EBI SCA Chart
###
from __future__ import unicode_literals

import base64, hashlib

from datetime import datetime


"""
    Extract the EBI SCA Experiment Id from an EBI SCA URL
"""
def create_an_ebi_sca_chart(a_url, a_experiment_id, a_chart_id, a_host, a_tmp_dir, a_output_dir):

    curl_command = 'curl -s \''
    jq_command = '\' | jq \''
    jq_params_prefix = '{ series, \"xAxis\": { \"visible\": true }, \"yAxis\": { \"visible\": true }, \"title\": { \"text\": \"'
    jq_params_suffix = '\", \"align\": \"center\", \"y\": 20 }, \"chart\": { \"type\": \"scatter\", \"height\":600, \"legend\": { \"enabled\": true } } }'

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H%M%S")

    working_file = a_tmp_dir + 'highcharts_input_' + date_time + '.json'
    output_file = a_output_dir + a_chart_id

    json_manipulation_1 = '\' > '
    json_manipulation_2 = ' && printf ",\\"constr\\": \\"Chart\\" }" >> '
    json_manipulation_3 = ' && printf \'%s\\n%s\\n\' "{\\"infile\\":\" \"$(cat '
    json_manipulation_4 = ')\" > '

    highcharts_manipulation_1 = ' && curl -H \'Expect:\' -H \'Content-Type: application/json\' -X POST --data-binary \"@'
    highcharts_manipulation_2 = '\" '
    highcharts_manipulation_3 = ' -o '

    highcharts_manipulation = highcharts_manipulation_1 + working_file + highcharts_manipulation_2 + a_host + highcharts_manipulation_3 + output_file

    highcharts_cleanup = ' && rm ' + working_file

    json_manipulation = json_manipulation_1 + working_file + json_manipulation_2 + working_file + json_manipulation_3 + working_file + json_manipulation_4 + working_file

    shell_command = curl_command + a_url + jq_command + jq_params_prefix + a_experiment_id + jq_params_suffix + json_manipulation + highcharts_manipulation + highcharts_cleanup

    return shell_command
