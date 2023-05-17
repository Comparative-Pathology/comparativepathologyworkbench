#!/usr/bin/python3
###!
# \file         untag_image.py
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
# This file contains the untag_image view routine
#
###
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from taggit.models import Tag

from matrices.models import Image

from matrices.routines import credential_exists
from matrices.routines import get_header_data


@login_required()
def untag_image(request, image_id, slug):
    """
    Un Tag an image
    """

    if credential_exists(request.user):

        tag = get_object_or_404(Tag, slug=slug)

        image = get_object_or_404(Image, pk=image_id)

        image.tags.remove(tag)

        if tag.taggit_taggeditem_items.count() <= 0:

            tag.delete()

        return HttpResponseRedirect(reverse('webgallery_edit_image', args=(image_id, )))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
