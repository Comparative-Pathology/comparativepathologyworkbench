#!/usr/bin/python3
###!
# \file         views_rest_cell.py
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
# The Cell View Set automatically provides `list`, `create`, `retrieve`,
# `update` and `destroy` actions.
###
from __future__ import unicode_literals

import os
import time
import requests

from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Q

from decouple import config

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from matrices.models import Cell

from matrices.serializers import CellSerializer


#
# BENCH CELL REST INTERFACE ROUTINES
#
class CellViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Cell.objects.all()

    serializer_class = CellSerializer

    permission_classes = ( permissions.IsAuthenticated, )


    def list(self, request, *args, **kwargs):

        return Response(data='Cell LIST Not Available')


    def create(self, request, *args, **kwargs):

        return Response(data='Cell CREATE Not Available')


    def retrieve(self, request, *args, **kwargs):

        return Response(data='Cell RETRIEVE Not Available')


    def update(self, request, *args, **kwargs):

        return Response(data='Cell UPDATE Not Available')


    def partial_update(self, request, *args, **kwargs):

        return Response(data='Cell PARTIAL UPDATE Not Available')


    def destroy(self, request, *args, **kwargs):

        return Response(data='Cell DELETE Not Available')
