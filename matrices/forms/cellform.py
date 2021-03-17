#!/usr/bin/python3
###!
# \file         cellform.py
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
# Form for editing Cells within Benches.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioSelect
from django.shortcuts import get_object_or_404


from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Blog
from matrices.models import Credential
from matrices.models import Authority
from matrices.models import CollectionAuthority
from matrices.models import Authorisation
from matrices.models import Collection
from matrices.models import CollectionAuthorisation


from matrices.routines import get_images_for_collection
from matrices.routines import get_active_collection_images_for_user


class CellForm(forms.ModelForm):

    class Meta:
        model = Cell
        fields = ('title', 'description', 'image')

    def __init__(self, user_id=None, image_id=None, matrix_id=None, *args, **kwargs):
        super(CellForm, self).__init__(*args, **kwargs)

        querysetActive = Image.objects.none()
        querysetSelected = Image.objects.none()

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        collection_image_list = list()

        if matrix.has_last_used_collection():

            querysetActive = get_images_for_collection(matrix.last_used_collection)

        else:

            querysetActive = get_active_collection_images_for_user(request.user)


        if image_id is not None:
            querysetSelected = Image.objects.filter(owner=user_id).filter(id=image_id)

        #if user_id is not None:
        #    querysetActive = Image.objects.filter(owner=user_id).filter(active=True)

        querysetCombined = querysetActive | querysetSelected

        self.fields['image'] = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=querysetCombined, empty_label=None)
        self.fields['image'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        """
        Shows an image with the label
        """
        image_id = conditional_escape(obj.identifier)
        viewer_url = conditional_escape(obj.viewer_url)
        birdseye_url = conditional_escape(obj.birdseye_url)
        name = conditional_escape(obj.name)

        label = """%s<a href="%s" target="_blank"><img  style="width:256px; height:256px; float: left" title="%s" src="%s" ></a>""" % (name, viewer_url, name, birdseye_url)

        return mark_safe(label)
