#!/usr/bin/python3
#
# ##
# \file         set_last_used_tag_in_matrix.py
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
# This file contains the set_last_used_tag_in_matrix view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


from matrices.models import Credential
from matrices.models import Matrix

from matrices.routines import get_or_none_tag


#
#   ACTIVATE AN IMAGE COLLECTION
#
@login_required
def set_last_used_tag_in_matrix(request, matrix_id, tag_id):

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        matrix = Matrix.objects.get_or_none(id=matrix_id)

        if matrix:

            tag = get_or_none_tag(tag_id)

            if tag:

                matrix.set_last_used_tag(tag)
                matrix.save()

                return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

            else:

                return HttpResponseRedirect(reverse('home', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
