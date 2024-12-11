#!/usr/bin/python3
#
# ##
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
# This file contains the Chart Tidy Up admin command
# ##
#
from __future__ import unicode_literals

import subprocess

from django.core.management.base import BaseCommand

from matrices.models import Image
from matrices.models import Document
from matrices.models import Artefact
from matrices.models import Server

from matrices.routines import escape_string
from matrices.routines import exists_image_in_table
from matrices.routines import exists_image_on_webserver
from matrices.routines import get_images_for_server
from matrices.routines import get_primary_cpw_environment


#
# The Chart Tidy Up admin command
#
class Command(BaseCommand):

    help = "Tidy Up the Charts stored on the webserver"

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--update",
            action="store_true",
            help="No update performed!",
        )

    def handle(self, *args, **options):

        update = False

        if options["update"]:

            update = True

        out_message = "Update                                                                     : {}".format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        environment = get_primary_cpw_environment()

        out_list_ebi = list()
        out_list_cpw = list()
        out_list_omero = list()
        rm_list = list()
        aux_rm_list = list()
        server_list = list()

        out_message = ""

        artefactDBTotal = 0
        imageEBIDBTotal = 0
        imageCPWDBTotal = 0
        imageOMERODBTotal = 0
        imageWebBeforeTotal = 0
        imageWebAfterTotal = 0
        imageDelTotal = 0

        documentDBTotal = Document.objects.count()

        #
        # BEFORE
        #
        out_message = "Total Number of Documents in Database BEFORE Cleanup                       : {}"\
            .format(documentDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        Document.objects.all().delete()

        artefact_list = Artefact.objects.all()
        artefactDBTotal = len(artefact_list)
        out_message = "Total Number of Artefacts (ZIPs etc) on Database BEFORE Cleanup            : {}"\
            .format(artefactDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_list_ebi = Image.objects.filter(server__type__name='EBI_SCA')
        imageEBIDBTotal = out_list_ebi.count()
        out_message = "Total Number of EBI Charts (PNGs etc) in Database BEFORE Cleanup           : {}"\
            .format(imageEBIDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_list_cpw = Image.objects.filter(server__type__name='CPW')
        imageCPWDBTotal = out_list_cpw.count()
        out_message = "Total Number of CPW Charts (PNGs etc) in Database BEFORE Cleanup           : {}"\
            .format(imageCPWDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        server_list = Server.objects.all()

        for server in server_list:

            if server.is_omero547() and not server.is_idr():

                out_list_omero = get_images_for_server(server)

                imageOMERODBTotal = imageOMERODBTotal + out_list_omero.count()

        out_message = "Total Number of OMERO Charts (PNGs etc) in Database BEFORE Cleanup         : {}"\
            .format(imageOMERODBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        ls_command = 'ls ' + environment.document_root
        process = subprocess.Popen(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)

        out_list = process.stdout.readlines()
        out_list_2 = out_list

        imageWebBeforeTotal = len(out_list)
        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) on Webserver BEFORE Cleanup : {}"\
            .format(imageWebBeforeTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        #
        # CLEANUP
        #
        for output in out_list_2:

            if not exists_image_in_table(output.strip()):

                new_output = environment.document_root + '/' + output.strip()

                artefact = Artefact.objects.get_or_none(location=new_output)

                if not artefact:

                    if not exists_image_on_webserver(output.strip()):

                        imageDelTotal = imageDelTotal + 1

                        rm_command = environment.document_root + '/' + output.strip()
                        rm_escaped = 'rm ' + escape_string(rm_command)

                        rm_list.append(rm_escaped)

        aux_rm_list = list(set(rm_list))

        for rm_command in aux_rm_list:

            self.stdout.write(self.style.SUCCESS(rm_command))

            if update:

                process = subprocess.Popen(rm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           universal_newlines=True)

        #
        # AFTER
        #
        ls_command = 'ls ' + environment.document_root
        process = subprocess.Popen(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)

        out_list_3 = process.stdout.readlines()

        imageWebAfterTotal = len(out_list_3)

        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) DELETED from Webserver      : {}"\
            .format(imageDelTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) on Webserver AFTER Cleanup  : {}"\
            .format(imageWebAfterTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        documentDBTotal = Document.objects.count()

        out_message = "Total Number of Documents in Database AFTER Cleanup                        : {}"\
            .format(documentDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        if update:

            Document.objects.all().delete()

        artefact_list = Artefact.objects.all()
        artefactDBTotal = len(artefact_list)
        out_message = "Total Number of Artefacts (ZIPs etc) on Database AFTER Cleanup             : {}"\
            .format(artefactDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_list_ebi = Image.objects.filter(server__type__name='EBI_SCA')
        imageEBIDBTotal = out_list_ebi.count()
        out_message = "Total Number of EBI Charts (PNGs etc) in Database AFTER Cleanup            : {}"\
            .format(imageEBIDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_list_cpw = Image.objects.filter(server__type__name='CPW')
        imageCPWDBTotal = out_list_cpw.count()
        out_message = "Total Number of CPW Charts (PNGs etc) in Database AFTER Cleanup            : {}"\
            .format(imageCPWDBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        imageOMERODBTotal = 0

        server_list = Server.objects.all()

        for server in server_list:

            if server.is_omero547() and not server.is_idr():

                out_list_omero = get_images_for_server(server)

                imageOMERODBTotal = imageOMERODBTotal + out_list_omero.count()

        out_message = "Total Number of OMERO Charts (PNGs etc) in Database AFTER Cleanup          : {}"\
            .format(imageOMERODBTotal)
        self.stdout.write(self.style.SUCCESS(out_message))

        ls_command = 'ls ' + environment.document_root
        process = subprocess.Popen(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)

        out_list = process.stdout.readlines()
        out_list_2 = out_list

        imageWebBeforeTotal = len(out_list)
        out_message = "Total Number of Files (ZIPs etc Plus PNGs etc) on Webserver AFTER Cleanup  : {}"\
            .format(imageWebBeforeTotal)
        self.stdout.write(self.style.SUCCESS(out_message))
