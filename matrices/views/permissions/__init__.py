#!/usr/bin/python3
###!
# \file         __init__.py
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
# BENCH AND COLLECTION AUTHORISATION ROUTINES
#
# def view_bench_authorisation(request, bench_authorisation_id):
# def new_bench_authorisation(request):
# def new_bench_bench_authorisation(request, matrix_id):
# def edit_bench_authorisation(request, bench_authorisation_id):
# def edit_bench_bench_authorisation(request, matrix_id, bench_authorisation_id):
# def delete_bench_authorisation(request, bench_authorisation_id):
#
# def view_collection_authorisation(request, collection_authorisation_id):
# def new_collection_authorisation(request):
# def new_collection_collection_authorisation(request, collection_id):
# def edit_collection_authorisation(request, collection_authorisation_id):
# def edit_collection_collection_authorisation(request, collection_id, collection_authorisation_id):
# def delete_collection_authorisation(request, collection_authorisation_id):
#
###

from .view_bench_authorisation import view_bench_authorisation
from .new_bench_authorisation import new_bench_authorisation
from .new_bench_bench_authorisation import new_bench_bench_authorisation
from .edit_bench_authorisation import edit_bench_authorisation
from .edit_bench_bench_authorisation import edit_bench_bench_authorisation
from .delete_bench_authorisation import delete_bench_authorisation
from .view_collection_authorisation import view_collection_authorisation
from .new_collection_authorisation import new_collection_authorisation
from .new_collection_collection_authorisation import new_collection_collection_authorisation
from .edit_collection_authorisation import edit_collection_authorisation
from .edit_collection_collection_authorisation import edit_collection_collection_authorisation
from .delete_collection_authorisation import delete_collection_authorisation
