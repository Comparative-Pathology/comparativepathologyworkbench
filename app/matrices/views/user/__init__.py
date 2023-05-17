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
# SIGNUP VIEW ROUTINES
#
# def signup(request):
# def account_activation_sent(request):
# def activate(request, uidb64, token):
#
###

from .account_activation_sent import account_activation_sent
from .activate import activate
from .login_user import login_user
from .signup import signup
from .change_password import *
from .change_password_done import *
from .reset_password import *
from .reset_password_done import *
from .reset_password_confirm import *
from .reset_password_complete import *
