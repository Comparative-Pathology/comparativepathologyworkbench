#!/usr/bin/python3
#
# ##
# \file         collection_delete_consequences.py
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
# Consequential Actions for Collection Deletes
# ##
#
from __future__ import unicode_literals

import subprocess

from django.apps import apps

from matrices.routines.get_active_collection_for_user import get_active_collection_for_user
from matrices.routines.get_collections_for_image import get_collections_for_image
from matrices.routines.exists_image_in_cells import exists_image_in_cells
from matrices.routines.exists_bench_for_last_used_collection import exists_bench_for_last_used_collection
from matrices.routines.get_benches_for_last_used_collection import get_benches_for_last_used_collection
from matrices.routines.exists_user_for_last_used_collection import exists_user_for_last_used_collection
from matrices.routines.get_users_for_last_used_collection import get_users_for_last_used_collection
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines.exists_collection_image_orders_for_collection_and_image_and_permitted \
    import exists_collection_image_orders_for_collection_and_image_and_permitted
from matrices.routines.get_collection_image_ordering_for_collection_and_image_and_user \
    import get_collection_image_ordering_for_collection_and_image_and_user
from matrices.routines.get_collection_image_orders_for_collection_and_ordering_equals \
    import get_collection_image_orders_for_collection_and_ordering_equals
from matrices.routines.get_collection_image_orders_for_collection_and_ordering_above \
    import get_collection_image_orders_for_collection_and_ordering_above


#
#   Consequential Actions for Collection Deletes
#
def collection_delete_consequences(a_user, a_collection):

    Collection = apps.get_model('matrices', 'Collection')

    environment = get_primary_cpw_environment()

    images = a_collection.get_all_images()

    collection_delete_flag = True

    for image in images:

        collection_list = get_collections_for_image(image)

        delete_flag = True

        for collection_other in collection_list:

            if a_collection != collection_other:

                delete_flag = False

        if image.exists_image_links():

            collection_delete_flag = False

        else:

            if delete_flag is False:

                if exists_image_in_cells(image):

                    collection_delete_flag = False

                else:

                    Collection.unassign_image(image, a_collection)

                    if exists_collection_image_orders_for_collection_and_image_and_permitted(a_collection,
                                                                                             image,
                                                                                             a_user):

                        ordering = get_collection_image_ordering_for_collection_and_image_and_user(a_collection,
                                                                                                   image,
                                                                                                   a_user)

                        collection_image_order_delete_list = \
                            get_collection_image_orders_for_collection_and_ordering_equals(a_collection, ordering)

                        for collection_image_order_delete in collection_image_order_delete_list:

                            collection_image_order_delete.delete()

                        collection_image_order_update_list = \
                            get_collection_image_orders_for_collection_and_ordering_above(a_collection, ordering)

                        for collection_image_order_update in collection_image_order_update_list:

                            collection_image_order_update.decrement_ordering()

                            collection_image_order_update.save()

                    if image.server.is_ebi_sca() or image.server.is_cpw():

                        image_path = environment.document_root + '/' + image.name

                        rm_command = 'rm ' + str(image_path)
                        rm_escaped = rm_command.replace("(","\(").replace(")","\)")

                        process = subprocess.Popen(rm_escaped,
                                                   shell=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   universal_newlines=True)

                    if image.server.is_omero547() and not image.server.is_idr():

                        image_path = environment.document_root + '/' + image.get_file_name_from_birdseye_url()

                        rm_command = 'rm ' + str(image_path)
                        rm_escaped = rm_command.replace("(","\(").replace(")","\)")

                        process = subprocess.Popen(rm_escaped,
                                                   shell=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   universal_newlines=True)

                    image.delete()

    if collection_delete_flag is True:

        if exists_bench_for_last_used_collection(a_collection):

            matrix_list = get_benches_for_last_used_collection(a_collection)

            for matrix in matrix_list:

                matrix.set_no_last_used_collection()

                matrix.save()

        if exists_user_for_last_used_collection(a_collection):

            user_list = get_users_for_last_used_collection(a_collection)

            for user in user_list:

                user.profile.set_last_used_collection(None)
                user.save()

        if a_collection == get_active_collection_for_user(a_user):

            a_user.profile.set_active_collection(None)
            a_user.save()

    return collection_delete_flag
