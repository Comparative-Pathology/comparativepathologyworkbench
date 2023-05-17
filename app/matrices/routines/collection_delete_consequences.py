#!/usr/bin/python3
###!
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
###
from __future__ import unicode_literals

import base64, hashlib

from django.apps import apps
from django.db.models import Q

from os import urandom

from matrices.routines.get_images_all_for_collection import get_images_all_for_collection
from matrices.routines.get_active_collection_for_user import get_active_collection_for_user
from matrices.routines.get_collections_for_image import get_collections_for_image
from matrices.routines.exists_image_in_cells import exists_image_in_cells
from matrices.routines.exists_bench_for_last_used_collection import exists_bench_for_last_used_collection
from matrices.routines.get_benches_for_last_used_collection import get_benches_for_last_used_collection
from matrices.routines.exists_user_for_last_used_collection import exists_user_for_last_used_collection
from matrices.routines.get_users_for_last_used_collection import get_users_for_last_used_collection


"""
    Consequential Actions for Collection Deletes
"""
def collection_delete_consequences(a_user, a_collection):

    Collection = apps.get_model('matrices', 'Collection')

    images = get_images_all_for_collection(a_collection)

    for image in images:

        collection_list = get_collections_for_image(image)

        delete_flag = False

        for collection_other in collection_list:

            if a_collection != collection_other:

                delete_flag = True

        if delete_flag == False:

            if not exists_image_in_cells(image):

                Collection.unassign_image(image, a_collection)

                image.delete()


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

