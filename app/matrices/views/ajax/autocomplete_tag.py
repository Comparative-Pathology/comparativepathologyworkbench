#!/usr/bin/python3
#
# ##
# \file         autocomplete_tag_2.py
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
# The autocomplete_tag_2 VIEW
# ##
#
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from taggit.models import Tag

from taggit.utils import parse_tags

from matrices.models import Image


#
#   The autocomplete_tag VIEW
#
def autocompleteTag(request, image_id):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        local_image = Image.objects.get_or_none(id=image_id)

        if local_image:

            if request.method == 'GET':

                search_term = request.GET.get('term', '').capitalize()

                search_qs = Tag.objects.filter(name__startswith=search_term)

                results = []

                for tag in search_qs:

                    results.append(tag.name)

                json_data = json.dumps(results)
                mimetype = 'application/json'

                return HttpResponse(json_data, mimetype)

            if request.method == 'POST':

                tags = request.POST.get('txtSearch', '').capitalize()

                tag_list = parse_tags(tags)

                for tag in tag_list:

                    local_image.tags.add(tag)

                return HttpResponseRedirect(reverse('webgallery_edit_image', args=(image_id, )))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
