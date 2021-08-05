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
# Do we have a valid EBI Single Cell Atlas URL?
###
from __future__ import unicode_literals

import base64, hashlib

from urllib.parse import urlparse


"""
    Do we have a Valid EBI Single Cell Atlas URL?
"""
def validate_an_ebi_sca_url(a_url):

    result = urlparse(a_url)

    if all([result.scheme, result.netloc, result.path, result.query]):

        server_url = result.netloc

        if server_url != "www.ebi.ac.uk":
            return False

        path_url = result.path

        path_array = path_url.split("/")

        if len(path_array) < 6:

            return False

        if path_array[1] != "gxa":

            return False

        if path_array[2] != "sc":

            return False

        if path_array[3] != "experiments":

            return False

        if path_array[5] != "results":

            return False

        if len(path_array) > 6:

            if path_array[6] != "tsne":

                return False


        query_url = result.query

        query_array = query_url.split("&")

        perplexity = ''
        k_value = ''
        geneId = ''
        colourBy = ''
        metadata = ''

        for array_entry in query_array:

            array_entry_array = array_entry.split("=")
            prefix = array_entry_array[0]
            suffix = array_entry_array[1]

            if prefix == 'perplexity':

                perplexity = suffix

            if prefix == 'k':

                k_value = suffix

            if prefix == 'geneId':

                geneId = suffix

            if prefix == 'colourBy':

                colourBy = suffix

            if prefix == 'metadata':

                metadata = suffix

        validClusterA = False
        validClusterB = False
        validGene = False

        if geneId == '' and colourBy == '' and k_value == '' and perplexity == '' and metadata == '':

            validClusterA = False
            validClusterB = False
            validGene = False

        else:

            if geneId != '' and colourBy != '' and k_value != '' and perplexity != '' and metadata != '':

                validClusterA = False
                validClusterB = False
                validGene = False

            else:

                if colourBy == 'metadata' and perplexity != '' and metadata != '':

                    validClusterA = False
                    validGene = False

                    if not perplexity.isnumeric():

                        validClusterB = False

                    else:

                        validClusterB = True

                else:

                    if colourBy == 'clusters' and k_value != '' and perplexity != '':

                        validClusterB = False
                        validGene = False

                        if not k_value.isnumeric() or not perplexity.isnumeric():

                            validClusterA = False

                        else:

                            validClusterA = True

                    else:

                        if geneId != '' and perplexity != '':

                            validClusterA = False
                            validClusterB = False

                            if not perplexity.isnumeric():

                                validGene = False

                            else:

                                if len(geneId) != 15:

                                    validGene = False

                                else:

                                    gene_prefix = geneId[0:4]
                                    gene_suffix = geneId[4:15]

                                    if gene_prefix != 'ENSG':

                                        validGene = False

                                    else:

                                        if not gene_suffix.isnumeric():

                                            validGene = False

                                        else:

                                            validGene = True

        if validClusterA or validClusterB or validGene:

            return True

        else:

            return False

    else:

        return False
