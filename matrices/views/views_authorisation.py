#!/usr/bin/python3
###!
# \file         views_authorisation.py
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
# This contains the collectivization, mailer, view_user, edit_user, delete_user,
# new_blog_credential, view_blog_credential, edit_blog_credential and
# delete_blog_credential views
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


from matrices.forms import CredentialForm
from matrices.forms import EditUserForm

from matrices.models import Credential
from matrices.models import Collection


from matrices.routines import exists_image_for_user
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_images_for_user
from matrices.routines import credential_exists
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data


HTTP_POST = 'POST'


#
# AUTHORSATION VIEW ROUTINES
#
# def collectivization(request):
# def mailer(request):
# def view_user(request, user_id):
# def edit_user(request, user_id):
# def delete_user(request, user_id):
# def new_blog_credential(request):
# def view_blog_credential(request, credential_id):
# def edit_blog_credential(request, credential_id):
# def delete_blog_credential(request, credential_id):
#

#
# SETUP DEFAULT COLLECTIONS VIEW
#
def collectivization(request):

    data = get_header_data(request.user)

    if request.user.is_superuser:

        user_list = User.objects.all()

        out_message_list = list()

        for user in user_list:

            imageCount = 0

            out_message = ""

            if exists_image_for_user(user):

                image_list = get_images_for_user(user)

                if exists_active_collection_for_user(user):

                    out_message = "Default Collection ALREADY exists for User {}".format( user.username )

                else:

                    collection = Collection.create("Default Collection", "Default Collection", True, user)

                    collection.save()

                    for image in image_list:

                        imageCount = imageCount + 1

                        Collection.assign_image(image, collection)

                    out_message = "Default Collection created for {} Images for User {}".format( imageCount, user.username )

            else:

                out_message = "NO Default Collection created for User {}".format( user.username )

            out_message_list.append(out_message)

        data.update({ 'out_message_list': out_message_list })

        return render(request, 'authorisation/collectivization.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# MAILER VIEW
#
def mailer(request):

    data = get_header_data(request.user)

    if request.user.is_superuser:

        now = timezone.now()

        subject = 'A Time Check'
        message = 'Here is the time : ' + str(now)
        email_from = config('DEFAULT_FROM_EMAIL')
        recipient_list = ['mike.wicks@gmail.com',]
        email_to = 'mike.wicks@gmail.com'

        data.update({ 'subject': subject, 'message': message, 'email_from': email_from, 'email_to': email_to })

        send_mail( subject, message, email_from, recipient_list, fail_silently=False )

    return render(request, 'authorisation/mailer.html', data)


#
# VIEW A USER
#
@login_required
def view_user(request, user_id):

    data = get_header_data(request.user)

    subject = get_object_or_404(User, pk=user_id)

    data.update({ 'subject': subject })

    return render(request, 'authorisation/detail_user.html', data)


#
# EDIT A USER
#
@login_required
def edit_user(request, user_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        subject = get_object_or_404(User, pk=user_id)

        data.update({ 'subject': subject })

        user = get_object_or_404(User, pk=request.user.id)

        if request.method == HTTP_POST:

            form = EditUserForm(request.POST, instance=subject)

            if form.is_valid:

                user = form.save(commit=False)

                user.save()

                return HttpResponseRedirect(reverse('authorisation', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = EditUserForm(instance=subject)

            data.update({ 'form': form })

        return render(request, 'authorisation/edit_user.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A USER
#
@login_required
def delete_user(request, user_id):

    if request.user.is_superuser:

        subject = get_object_or_404(User, pk=user_id)

        subject.delete()

        return HttpResponseRedirect(reverse('authorisation', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW USER BLOG CREDENTIAL
#
@login_required
def new_blog_credential(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = CredentialForm(request.POST)

            if form.is_valid:

                credential = form.save(commit=False)

                credential.set_owner(request.user)

                credential.save()

                return HttpResponseRedirect(reverse('authorisation', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = CredentialForm()

            data.update({ 'form': form })

        return render(request, 'authorisation/new_blog_credential.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# VIEW A USER BLOG CREDENTIAL
#
@login_required
def view_blog_credential(request, credential_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        credential = get_object_or_404(Credential, pk=credential_id)

        data.update({ 'credential_id': credential_id, 'credential': credential })

        return render(request, 'authorisation/detail_blog_credential.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT A USER BLOG CREDENTIAL
#
@login_required
def edit_blog_credential(request, credential_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        credential = get_object_or_404(Credential, pk=credential_id)

        if request.method == HTTP_POST:

            form = CredentialForm(request.POST, instance=credential)

            if form.is_valid:

                credential = form.save(commit=False)

                credential.set_owner(request.user)

                credential.save()

                return HttpResponseRedirect(reverse('authorisation', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'credential': credential })

        else:

            form = CredentialForm(instance=credential)

            data.update({ 'form': form, 'credential': credential })

        return render(request, 'authorisation/edit_blog_credential.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A USER BLOG CREDENTIAL
#
@login_required
def delete_blog_credential(request, credential_id):

    if request.user.is_superuser:

        credential = get_object_or_404(Credential, pk=credential_id)

        credential.delete()

        return HttpResponseRedirect(reverse('authorisation', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
