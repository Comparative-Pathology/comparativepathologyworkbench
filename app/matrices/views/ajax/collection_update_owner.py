#!/usr/bin/python3
###!
# \file         collection_update_owner.py
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
# This file contains the AJAX collection_update_owner view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.forms import CollectionOwnerSelectionForm

from matrices.models import Collection
from matrices.models import CollectionAuthorisation

from matrices.routines import credential_exists
from matrices.routines import simulate_network_latency
from matrices.routines import collection_authorisation_exists_for_collection_and_permitted
from matrices.routines.get_active_collection_for_user import get_active_collection_for_user


#
# Re-Allocate the Collectio Owner
#
@login_required()
def collection_update_owner(request, collection_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied

    collection = get_object_by_uuid_or_404(Collection, collection_id)
    old_owner = collection.owner

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = CollectionOwnerSelectionForm(instance=collection, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            new_owner = object.owner

            if collection == get_active_collection_for_user(old_owner):

                old_owner.profile.set_active_collection(None)
                old_owner.save()

            if not collection_authorisation_exists_for_collection_and_permitted(collection, old_owner):

                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection) &
                                                                                   Q(permitted=new_owner))

                collection_authorisation_new = \
                    CollectionAuthorisation.create(collection,
                                                   old_owner,
                                                   collection_authorisation_old.collection_authority)

                collection_authorisation_old.delete()
                collection_authorisation_new.save()

            image_list = collection.get_all_images()

            for image in image_list:

                image.set_owner(new_owner)
                image.save()

            object.save()

            messages.success(request, 'New Owner ' + str(collection.owner.username) +
                             ' for Collection ' + "{:06d}".format(collection.id) + '!')

    else:

        form = CollectionOwnerSelectionForm(instance=collection, initial={'owner': collection.owner.id}, )

    return render(request, template_name, {
        'form': form,
        'object': collection
    })
