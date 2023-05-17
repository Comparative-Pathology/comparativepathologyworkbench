#!/usr/bin/python3
###!
# \file         admin.py
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
# This allows the Type, Protocol, Command, Blog, Credential, Authority and
# CollectionAuthority models to be managed via the Django Admin Web Interface
###
from django.contrib import admin

from .models import Type
from .models import Protocol
from .models import Command
from .models import Blog
from .models import Credential
from .models import Authority
from .models import CollectionAuthority

admin.site.register(Type)
admin.site.register(Protocol)
admin.site.register(Command)
admin.site.register(Blog)
admin.site.register(Credential)
admin.site.register(Authority)
admin.site.register(CollectionAuthority)
