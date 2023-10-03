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
# AUTHORSATION VIEW ROUTINES
# 
# def delete_blog_credential(request, credential_id):
# def delete_user(request, user_id):
# def edit_blog_credential(request, credential_id):
# def edit_user(request, user_id):
# def edit_constrained_user(request, user_id):
# def new_blog_credential(request):
# def new_blog_credential(request):
# def view_blog_credential(request, credential_id):
# def view_user(request, user_id):
# def view_constrained_user(request, user_id):
#
###

from .delete_blog_credential import delete_blog_credential
from .delete_user import delete_user
from .edit_blog_credential import edit_blog_credential
from .edit_user import edit_user
from .edit_constrained_user import edit_constrained_user
from .new_blog_credential import new_blog_credential
from .nginx_accel import nginx_accel
from .view_blog_credential import view_blog_credential
from .view_user import view_user
from .view_constrained_user import view_constrained_user
