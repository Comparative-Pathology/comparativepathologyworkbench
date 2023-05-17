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
# MAINTENANCE ROUTINES
#
# def view_blog_command(request, blog_id):
# def new_blog_command(request):
# def edit_blog_command(request, blog_id):
# def delete_blog_command(request, blog_id):
#
# def view_command(request, command_id):
# def new_command(request):
# def edit_command(request, command_id):
# def delete_command(request, command_id):
#
# def view_protocol(request, protocol_id):
# def new_protocol(request):
# def edit_protocol(request, protocol_id):
# def delete_protocol(request, protocol_id):
#
# def view_type(request, type_id):
# def new_type(request):
# def edit_type(request, type_id):
# def delete_type(request, type_id):
#
# def view_bench_authority(request, bench_authority_id):
# def new_bench_authority(request):
# def edit_bench_authority(request, bench_authority_id):
# def delete_bench_authority(request, bench_authority_id):
#
# def view_collection_authority(request, collection_authority_id):
# def new_collection_authority(request):
# def edit_collection_authority(request, collection_authority_id):
# def delete_collection_authority(request, collection_authority_id):
#
# def view_location(request, location_id):
# def new_location(request):
# def edit_location(request, location_id):
# def delete_location(request, location_id):
#
# def view_environment(request, environment_id):
# def new_environment(request):
# def edit_environment(request, environment_id):
# def delete_environment(request, environment_id):
#
###

from .delete_bench_authority import delete_bench_authority
from .delete_blog_command import delete_blog_command
from .delete_collection_authority import delete_collection_authority
from .delete_command import delete_command
from .delete_protocol import delete_protocol
from .delete_type import delete_type
from .delete_location import delete_location
from .delete_environment import delete_environment
from .edit_bench_authority import edit_bench_authority
from .edit_blog_command import edit_blog_command
from .edit_collection_authority import edit_collection_authority
from .edit_command import edit_command
from .edit_protocol import edit_protocol
from .edit_type import edit_type
from .edit_location import edit_location
from .edit_environment import edit_environment
from .new_bench_authority import new_bench_authority
from .new_blog_command import new_blog_command
from .new_collection_authority import new_collection_authority
from .new_command import new_command
from .new_protocol import new_protocol
from .new_type import new_type
from .new_location import new_location
from .new_environment import new_environment
from .view_bench_authority import view_bench_authority
from .view_blog_command import view_blog_command
from .view_collection_authority import view_collection_authority
from .view_command import view_command
from .view_protocol import view_protocol
from .view_type import view_type
from .view_location import view_location
from .view_environment import view_environment
