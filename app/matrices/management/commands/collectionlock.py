#!/usr/bin/python3
#
# ##
# \file         collectionlock.py
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
# This file contains the Collection Lock admin command USING a Task if possible
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from matrices.models import Collection

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

from background.tasks import lock_collection_task


#
#   The Collection Lock admin command
#
class Command(BaseCommand):
    help = "Lock Collection USING a Task"

    def add_arguments(self, parser):

        parser.add_argument('collection_lock', type=str, help='Indicates the Id of the Collection to be locked')

        # Named (optional) arguments
        parser.add_argument(
            "--update",
            action="store_true",
            help="No update performed!",
        )

    def handle(self, *args, **options):

        collection_lock = options['collection_lock']

        update = False

        if options["update"]:

            update = True

        out_message = "Update                                                   : {}"\
            .format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Lock Collection                                          : {}"\
            .format(collection_lock)
        self.stdout.write(self.style.SUCCESS(out_message))

        environment = get_primary_cpw_environment()

        out_message = ""
        task_message = ""

        collection_list = list()

        if collection_lock.lower() == 'all':

            collection_list = Collection.objects.all().order_by('id')

        else:

            collection_list = Collection.objects.filter(id=collection_lock).order_by('id')

        for collection in collection_list:

            if update:

                if environment.is_background_processing():

                    result = lock_collection_task.delay(collection.id)

                    if result.ready():

                        task_message = result.get(timeout=1)
                        self.stdout.write(self.style.SUCCESS(task_message))

                else:

                    collection.set_locked()

                    collection.save()

            out_message = "Program collectionlocktask : Collection CPW:{0:06d} lock: {1}!!"\
                .format(collection.id, collection.locked)
            self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Program : Lock Collection TASK Complete!!"
        self.stdout.write(self.style.SUCCESS(out_message))
