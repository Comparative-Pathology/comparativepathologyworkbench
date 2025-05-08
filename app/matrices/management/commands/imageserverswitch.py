#!/usr/bin/python3
#
# ##
# \file         imageserverswitch.py
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
# This file contains the Image Server Switch admin command USING a Task if possible
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from matrices.models import Server
from matrices.models import Image

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

from background.tasks import switch_image_server_task


#
#   The Image Server Switch admin command
#
class Command(BaseCommand):

    help = "Switch Image to a New Server USING a Task"

    def add_arguments(self, parser):

        parser.add_argument('-i',
                            '--image',
                            type=str,
                            help='Supply an Image Id', )
        parser.add_argument('-s',
                            '--server',
                            type=str,
                            help='Supply an Server Id', )

        # Named (optional) arguments
        parser.add_argument("--update",
                            action="store_true",
                            help="No update performed!", )

    def handle(self, *args, **options):

        image_id = options['image']
        new_server_id = options['server']

        update = False
        new_server_present = False
        old_server_present = False

        if options["update"]:

            update = True

        out_message = "Update                                                   : {}"\
            .format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Image Id                                                 : {}"\
            .format(image_id)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Server Id                                                : {}"\
            .format(new_server_id)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = ""
        task_message = ""

        new_server_data = {}
        old_server_data = {}

        image = None
        new_server = None
        old_server = None

        environment = get_primary_cpw_environment()

        image = Image.objects.get_or_none(id=int(image_id))

        if image:

            old_server = Server.objects.get_or_none(id=image.server.id)

            if old_server:

                if old_server.is_omero547():

                    if environment.is_web_gateway() or old_server.is_idr():

                        old_server_data = old_server.get_imaging_server_image_json(image.identifier)

                    else:

                        if environment.is_blitz_gateway():

                            old_server_data = old_server.get_imaging_server_image_json_blitz(image.identifier,
                                                                                             environment.gateway_port)

            new_server = Server.objects.get_or_none(id=new_server_id)

            if new_server:

                if new_server.is_omero547():

                    if environment.is_web_gateway() or new_server.is_idr():

                        new_server_data = new_server.get_imaging_server_image_json(image)

                    else:

                        if environment.is_blitz_gateway():

                            new_server_data = new_server.get_imaging_server_image_json_blitz(image.identifier,
                                                                                             environment.gateway_port)

            old_image_data = old_server_data['image']
            new_image_data = new_server_data['image']

            old_image_name = old_image_data['name']
            new_image_name = new_image_data['name']

            if old_image_name == 'ERROR':

                old_server_present = False

            else:

                old_server_present = True

            if new_image_name == 'ERROR':

                new_server_present = False

            else:

                new_server_present = True

            if update is True and old_server_present is False and new_server_present is True:

                group = new_server_data['group']
                group_name = group['name']

                projects = new_server_data['projects']
                project = projects[0]
                project_name = project['name']

                datasets = new_server_data['datasets']
                dataset = datasets[0]
                dataset_name = dataset['name']

                full_image_name = group_name + "/" + project_name + "/" + dataset_name + "/" + new_image_name

                if environment.is_background_processing():

                    result = switch_image_server_task.delay(image.id, full_image_name, new_server.id)

                    if result.ready():

                        task_message = result.get(timeout=1)
                        self.stdout.write(self.style.SUCCESS(task_message))

                else:

                    image.name = full_image_name
                    image.server = new_server
                    image.save()

                    out_message = "Program imageserverswitch UPDATE: Image " + str(image.id) + \
                        " named: " + str(image.name) + \
                        " has NEW server: " + str(image.server.name)

                    self.stdout.write(self.style.SUCCESS(out_message))

            else:

                out_message = "Program imageserverswitch NO UPDATE!"
                self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Program : imageserverswitch Complete!!"
        self.stdout.write(self.style.SUCCESS(out_message))
