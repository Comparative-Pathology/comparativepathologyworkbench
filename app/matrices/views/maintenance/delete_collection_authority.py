#!/usr/bin/python3
#
# ##
# \file         delete_collection_authority.py
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
# This file contains the delete_collection_authority view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import CollectionAuthority

from matrices.routines import exists_collection_authorisation_viewer


#
#   DELETE A COLLECTION AUTHORITY
#
@login_required
def delete_collection_authority(request, collection_authority_id):

    if request.user.is_superuser:

        collection_authority = CollectionAuthority.objects.get_or_none(id=collection_authority_id)

        if collection_authority:

            if collection_authority.is_viewer() and exists_collection_authorisation_viewer():

                messages.error(request, 'CPW_WEB:0480 Collection Authority ' + collection_authority.name +
                               ' NOT Deleted - Collection Authorisations still exist!')

            else:

                messages.success(request, 'Collection Authority ' + collection_authority.name + ' Deleted!')

                collection_authority.delete()

            return HttpResponseRedirect(reverse('maintenance', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
