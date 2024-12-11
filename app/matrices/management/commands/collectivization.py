#!/usr/bin/python3
#
# ##
# \file         collectivization.py
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
# This file contains the Setup Default Collections admin command
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from matrices.models import Collection

from matrices.routines import exists_image_for_user
from matrices.routines import get_images_for_user


#
# The Setup Default Collections admin command
#
class Command(BaseCommand):

    help = "Setup Default Collections for each User"

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

        out_message = "Update                                                 : {}"\
            .format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        user_list = User.objects.all()

        for user in user_list:

            imageCount = 0

            if exists_image_for_user(user):

                image_list = get_images_for_user(user)

                if user.profile.has_active_collection():

                    out_message = "Default Collection ALREADY exists for User             : {}"\
                        .format(user.username)
                    self.stdout.write(self.style.SUCCESS(out_message))

                else:

                    if update:

                        collection = Collection.create("Default Collection", "Default Collection", True, user)

                        collection.save()

                        for image in image_list:

                            imageCount = imageCount + 1

                            Collection.assign_image(image, collection)

                        out_message = "Default Collection created for {} Images for User      : {}"\
                            .format(imageCount, user.username)
                        self.stdout.write(self.style.SUCCESS(out_message))

            else:

                out_message = "NO Default Collection created for User                 : {}"\
                    .format(user.username)
                self.stdout.write(self.style.SUCCESS(out_message))
