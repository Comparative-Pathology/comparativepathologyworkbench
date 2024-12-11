#!/usr/bin/python3
#
# ##
# \file         collectionimageorders.py
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
# This file contains the Populate Collection Image Orders admin command
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from matrices.models import Collection
from matrices.models import CollectionAuthorisation
from matrices.models import CollectionImageOrder


#
#   The Populate Collection Image Orders admin command
#
class Command(BaseCommand):

    help = "Populate Collection Image Orders for each User"

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

        collectionimageorder_count = CollectionImageOrder.objects.all().count()

        if update is True:

            CollectionImageOrder.objects.all().delete()

            out_message = "Collection Image Orders Deleted                        : {}"\
                .format(str(collectionimageorder_count))
            self.stdout.write(self.style.SUCCESS(out_message))

        collection_list = Collection.objects.all()

        order_count = 0

        for collection in collection_list:

            collection_image_list = collection.images.all()

            collection_authorisation_list = CollectionAuthorisation.objects.filter(collection__id=collection.id)

            row_count = 1

            for image in collection_image_list:

                collectionimageorder = CollectionImageOrder.create(collection,
                                                                   image,
                                                                   collection.owner,
                                                                   row_count)

                if update is True:

                    collectionimageorder.save()

                else:

                    out_message = "Collection Image Order Created                         : {}"\
                        .format(str(collectionimageorder))
                    self.stdout.write(self.style.SUCCESS(out_message))

                order_count = order_count + 1

                for collection_authorisation in collection_authorisation_list:

                    collectionimageorder = CollectionImageOrder.create(collection,
                                                                       image,
                                                                       collection_authorisation.permitted,
                                                                       row_count)

                    if update is True:

                        collectionimageorder.save()

                    else:

                        out_message = "Collection Image Order Created                         : {}"\
                            .format(str(collectionimageorder))
                        self.stdout.write(self.style.SUCCESS(out_message))

                    order_count = order_count + 1

                row_count = row_count + 1

        out_message = "Number of Collection Image Orders Created              : {}"\
            .format(order_count)
        self.stdout.write(self.style.SUCCESS(out_message))
