#!/usr/bin/python3
#
# ##
# \file         collection_ordering_selection.py
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
# This file contains the AJAX bench_collection_update view routine
# ##
#
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.forms import ImageSummaryOrderingForm

from matrices.models import Collection
from matrices.models import CollectionImageOrder
from matrices.models import Credential
from matrices.models import Image

from matrices.routines import is_request_ajax


#
#   Select a Collection
#
@login_required()
def collection_ordering_selection(request, collection_id, image_id, permitted_id):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    object = Collection.objects.get_or_none(id=collection_id)

    if not object:

        raise PermissionDenied

    template_name = 'frontend_forms/generic_form_inner.html'

    collection = Collection.objects.get(id=int(collection_id))

    image = Image.objects.get(id=int(image_id))

    permitted_user = User.objects.get(id=int(permitted_id))

    cio_queryset = CollectionImageOrder.objects.filter(permitted=permitted_user)\
        .filter(collection=collection)\
        .order_by('ordering')

    my_ordering_list = []

    for cio in cio_queryset:

        my_ordering_list.append((str(cio.ordering), str(cio.ordering)))

    cio_queryset_selected = CollectionImageOrder.objects.filter(permitted=permitted_user)\
        .filter(collection=collection)\
        .filter(image=image)\
        .order_by('ordering')

    my_init_ordering = 1

    cio_for_update = None

    for cio_selected in cio_queryset_selected:

        my_init_ordering = cio_selected.ordering

        cio_for_update = cio_selected

    if request.method == 'POST':

        form = ImageSummaryOrderingForm(my_ordering_list, init_ordering=my_init_ordering, data=request.POST)

        if form.is_valid():

            new_ordering = form.cleaned_data['ordering']

            if int(new_ordering) == int(my_init_ordering):

                messages.success(request, 'Image ' + str(image_id) + ' Ordering NOT Changed!')

            if int(new_ordering) > int(my_init_ordering):

                cio_gt_queryset = CollectionImageOrder.objects.filter(permitted=permitted_user)\
                    .filter(collection=collection)\
                    .filter(ordering__gt=int(my_init_ordering))\
                    .filter(ordering__lte=int(new_ordering))\
                    .order_by('ordering')

                for cio_gt in cio_gt_queryset:

                    cio_gt.decrement_ordering()

                    cio_gt.save()

                cio_for_update.ordering = int(new_ordering)

                cio_for_update.save()

                messages.success(request, 'Image ' + str(image_id) + ' Ordering GT Old Ordering!')

            if int(new_ordering) < int(my_init_ordering):

                cio_lt_queryset = CollectionImageOrder.objects.filter(permitted=permitted_user)\
                    .filter(collection=collection)\
                    .filter(ordering__gte=int(new_ordering))\
                    .filter(ordering__lt=int(my_init_ordering))\
                    .order_by('ordering')

                for cio_lt in cio_lt_queryset:

                    cio_lt.increment_ordering()

                    cio_lt.save()

                cio_for_update.ordering = int(new_ordering)

                cio_for_update.save()

                messages.success(request, 'Image ' + str(image_id) + ' Ordering LT Old Ordering!')

    else:

        form = ImageSummaryOrderingForm(my_ordering_list, init_ordering=my_init_ordering)

    return render(request, template_name, {'form': form,
                                           'object': object})
