#!/usr/bin/python3
###!
# \file         charttidyup.py
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
# This file contains the collectivization view routine
#
###
from __future__ import unicode_literals

import subprocess

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from decouple import config

from matrices.models import Image
from matrices.models import Document
from matrices.models import Artefact

from matrices.routines import get_header_data
from matrices.routines import exists_artefact_in_table
from matrices.routines import exists_image_in_table
from matrices.routines import exists_image_on_webserver

#
# SETUP DEFAULT COLLECTIONS VIEW
#
def charttidyup(request):


    data = get_header_data(request.user)

    if request.user.is_superuser:

        documentDBTotal = Document.objects.count()

        Document.objects.all().delete()

        image_list1 = Image.objects.filter(server__type__name='EBI_SCA')
        image_list2 = Image.objects.filter(server__type__name='CPW')
        artefact_list = Artefact.objects.all()

        out_message_list = list()
        out_list = list()
        out_list_2 = list()
        rm_list = list()
        aux_rm_list = list()

        out_message = ""

        artefactDBTotal = 0
        imageDBTotal = 0
        imageWebBeforeTotal = 0
        imageWebAfterTotal = 0
        imageDelTotal = 0

        imageDBTotal = image_list1.count() + image_list2.count()

        ls_command = 'ls ' + config('HIGHCHARTS_OUTPUT_DIR')
        process = subprocess.Popen(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        out_list = process.stdout.readlines()
        out_list_2 = out_list

        imageWebBeforeTotal = len(out_list)
        artefactDBTotal = len(artefact_list)

        out_message = "Total Number of Documents in Database = {}".format( documentDBTotal )
        out_message_list.append(out_message)

        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) on Webserver BEFORE Cleanup = {}".format( imageWebBeforeTotal )
        out_message_list.append(out_message)

        out_message = "Total Number of Charts (PNGs etc) in Database = {}".format( imageDBTotal )
        out_message_list.append(out_message)

        out_message = "Total Number of Artefacts (ZIPs etc) on Database BEFORE Cleanup = {}".format( artefactDBTotal )
        out_message_list.append(out_message)

        for output in out_list_2:

            if not exists_image_in_table(output.strip()):

                new_output = settings.MEDIA_ROOT + "/" + output.strip()

                if not exists_artefact_in_table(new_output):

                    if not exists_image_on_webserver(output.strip()):

                        imageDelTotal = imageDelTotal + 1

                        rm_command = 'rm ' + config('HIGHCHARTS_OUTPUT_DIR') + output.strip()

                        rm_list.append(rm_command)

        aux_rm_list = list(set(rm_list))

        out_message_list = out_message_list + aux_rm_list

        for rm_command in aux_rm_list:

            process = subprocess.Popen(rm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        ls_command = 'ls ' + config('HIGHCHARTS_OUTPUT_DIR')
        process = subprocess.Popen(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        out_list_3 = process.stdout.readlines()

        imageWebAfterTotal = len(out_list_3)

        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) DELETED from Webserver = {}".format( imageDelTotal )
        out_message_list.append(out_message)

        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) on Webserver AFTER Cleanup = {}".format( imageWebAfterTotal )
        out_message_list.append(out_message)

        data.update({ 'out_message_list': out_message_list })

        return render(request, 'authorisation/charttidyup.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
