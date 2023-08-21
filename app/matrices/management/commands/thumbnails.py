#!/usr/bin/python3
###!
# \file         thumbnails.py
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
# This file contains the Generate Thumbnails admin command
#
###
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from datetime import datetime

from django.conf import settings

from decouple import config

from omero.gateway import BlitzGateway
from io import BytesIO
from PIL import Image as ImageOME

from matrices.models import Image
from matrices.models import Server

from matrices.routines import AESCipher
from matrices.routines import get_header_data
from matrices.routines import get_images_for_server
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
#
# The Generate Thumbnails admin command
#
class Command(BaseCommand):
    help = "Generate Thumbnails"


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
            
        out_message = "Update                                   : {}".format( update )
        self.stdout.write(self.style.SUCCESS(out_message))

        environment  = get_primary_cpw_environment()

        imageTotal = 0
        imageChanged = 0
        imageNotChanged = 0
        imageNotExist = 0

        out_message = ""

        server_list = Server.objects.all()

        for server in server_list:

            if server.is_omero547() and not server.is_idr():

                password = ''

                conn = None

                cipher = AESCipher(config('CPW_CIPHER_STRING'))
                byte_password = cipher.decrypt(server.pwd)
                password = byte_password.decode('utf-8')

                conn = BlitzGateway(server.uid, password, host=server.url_server, port=4064, secure=True)
                conn.connect()

                image_list = get_images_for_server(server)

                for image in image_list:

                    imageTotal = imageTotal + 1

                    if "webgateway" in image.birdseye_url:

                        image_ome = conn.getObject("Image", str(image.identifier))

                        if image_ome == None:

                            imageNotExist = imageNotExist + 1

                        else:

                            img_data = image_ome.getThumbnail(300)
                            rendered_thumb = ImageOME.open(BytesIO(img_data))

                            now = datetime.now()
                            date_time = now.strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

                            new_chart_id = date_time + '_' + str(image.identifier) + '_' + 'thumbnail.jpg'

                            new_birdseye_url = 'http://' + environment.web_root + '/' + new_chart_id

                            new_full_path = str(settings.MEDIA_ROOT) + '/' + new_chart_id

                            image.set_birdseye_url(new_birdseye_url)

                            if update: 

                                image.save()

                                rendered_thumb.save(new_full_path)

                            imageChanged = imageChanged + 1


                    else:

                        imageNotChanged = imageNotChanged + 1

                conn.close()


        out_message = "Total Number of Images                   : {}".format( imageTotal )
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Images that Do Not Exist : {}".format( imageNotExist )
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Images Changed           : {}".format( imageChanged )
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Images Not Changed       : {}".format( imageNotChanged )
        self.stdout.write(self.style.SUCCESS(out_message))

