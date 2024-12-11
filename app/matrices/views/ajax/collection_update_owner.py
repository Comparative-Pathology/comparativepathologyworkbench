#!/usr/bin/python3
#
# ##
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
# This file contains the AJAX collection_update_owner view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render

from matrices.forms import CollectionOwnerSelectionForm

from matrices.models import Collection
from matrices.models import CollectionAuthority
from matrices.models import CollectionAuthorisation
from matrices.models import CollectionImageOrder
from matrices.models import Credential

from matrices.routines import collection_authorisation_exists_for_collection_and_permitted
from matrices.routines import exists_collection_image_orders_for_collection_and_permitted
from matrices.routines import get_collection_image_orders_for_collection_and_permitted_orderedby_ordering

#
#   Re-Allocate the Collectio Owner
#
@login_required()
def collection_update_owner(request, collection_id):

    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    collection = Collection.objects.get_or_none(id=collection_id)

    if not collection:

        raise PermissionDenied

    existing_owner = collection.owner

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = CollectionOwnerSelectionForm(instance=collection, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            new_owner = object.owner

            if collection == existing_owner.profile.active_collection:

                existing_owner.profile.set_active_collection(None)
                existing_owner.save()

            if not collection_authorisation_exists_for_collection_and_permitted(collection, existing_owner):

                redundant_collection_authority = ''

                if collection_authorisation_exists_for_collection_and_permitted(collection, new_owner):

                    collection_authorisation_redundant = CollectionAuthorisation.objects.get(Q(collection=collection) &
                                                                                             Q(permitted=new_owner))

                    redundant_collection_authority = collection_authorisation_redundant.collection_authority

                    collection_authorisation_redundant.delete()

                else:

                    redundant_collection_authority = CollectionAuthority.objects.get(Q(name='VIEWER'))

                collection_authorisation_replacement = \
                    CollectionAuthorisation.create(collection,
                                                   existing_owner,
                                                   redundant_collection_authority)

                collection_authorisation_replacement.save()

                if exists_collection_image_orders_for_collection_and_permitted(collection, new_owner):

                    collection_image_ordering_redundant_list = \
                        get_collection_image_orders_for_collection_and_permitted_orderedby_ordering(collection,
                                                                                                    existing_owner)

                    for collection_image_ordering_redundant in collection_image_ordering_redundant_list:

                        collectionimageorder_replacement = \
                            CollectionImageOrder.create(collection,
                                                        collection_image_ordering_redundant.image,
                                                        existing_owner,
                                                        collection_image_ordering_redundant.ordering)

                        collectionimageorder_replacement.save()

                    for collection_image_ordering_redundant in collection_image_ordering_redundant_list:

                        collection_image_ordering_redundant.delete()

                else:

                    collection_image_ordering_redundant_list = \
                        get_collection_image_orders_for_collection_and_permitted_orderedby_ordering(collection,
                                                                                                    existing_owner)

                    for collection_image_ordering_redundant in collection_image_ordering_redundant_list:

                        collectionimageorder_replacement = \
                            CollectionImageOrder.create(collection,
                                                        collection_image_ordering_redundant.image,
                                                        new_owner,
                                                        collection_image_ordering_redundant.ordering)

                        collectionimageorder_replacement.save()

            image_list = collection.get_all_images()

            for image in image_list:

                image.set_owner(new_owner)
                image.save()

            object.save()

            messages.success(request, 'New Owner ' + str(collection.owner.username) +
                             ' for Collection ' + collection.get_formatted_id() + '!')

    else:

        form = CollectionOwnerSelectionForm(instance=collection, initial={'owner': collection.owner.id}, )

    return render(request, template_name, {'form': form,
                                           'object': collection})
