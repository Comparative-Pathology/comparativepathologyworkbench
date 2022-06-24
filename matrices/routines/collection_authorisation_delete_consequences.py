#!/usr/bin/python3
###!
# \file         collection_authorisation_delete_consequences.py
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
# Consequential Actions for Collection Authorisation Deletes
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from matrices.routines.exists_benches_for_last_used_collection import exists_benches_for_last_used_collection
from matrices.routines.get_benches_for_last_used_collection import get_benches_for_last_used_collection


"""
    Consequential Actions for Collection Authorisation Deletes
"""
def collection_authorisation_delete_consequences(a_user, a_collection):

    if exists_benches_for_last_used_collection(a_collection):

        matrix_list = get_benches_for_last_used_collection(a_collection)

        for matrix in matrix_list:

            if matrix.owner == a_user:

                matrix.set_no_last_used_collection()

                matrix.save()
