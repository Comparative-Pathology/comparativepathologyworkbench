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
#
# THE HOST VIEW ROUTINES
#
# def home(request):
# def view_server(request, server_id):
# def new_server(request):
# def edit_server(request, server_id):
# def delete_server(request, server_id):
# def authorisation(request):
# def maintenance(request):
#
# def list_imaging_hosts(request):
# def list_image_cart(request):
#
# def list_bench_authorisation(request):
# def list_my_bench_authorisation(request):
# def list_user_bench_bench_authorisation(request, user_id):
#
# def list_collection_authorisation(request):
# def list_my_collection_authorisation(request):
#
###

from .authorisation import authorisation
from .maintenance import maintenance

from .home import home
from .list_collection import *
from .list_image_cart import list_image_cart
from .list_imaging_hosts import list_imaging_hosts
from .list_matrix import *
from .list_bench_authorisation import list_bench_authorisation
from .list_my_bench_authorisation import list_my_bench_authorisation
from .list_user_bench_authorisation import list_user_bench_authorisation
from .list_collection_authorisation import list_collection_authorisation
from .list_my_collection_authorisation import list_my_collection_authorisation
from .list_user_collection_authorisation import list_user_collection_authorisation

from .execute_command import execute_command
