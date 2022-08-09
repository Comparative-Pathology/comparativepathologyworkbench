#!/usr/bin/python3
###!
# \file         blocked_adaptor.py
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
# Restricts editing to owner and superuser.
###
from django import forms

from inlineedit.adaptors import BasicAdaptor


class BlockedAdaptor(BasicAdaptor):

    # "Demonstrate adaptor level permission setting"
    def has_edit_perm(self, user):

        model_name = self._model.__class__.__name__

        owner = ''

        if model_name == 'Cell':

            owner = self._model.matrix.owner

        else:

            owner = self._model.owner

        allow_flag = False

        if owner == user:

            allow_flag = True

        else:

            if user.is_superuser:

                allow_flag = True


        return allow_flag
