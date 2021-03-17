#!/usr/bin/python3
###!
# \file         views_maintenance.py
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
# This contains the view_blog_command, new_blog_command, edit_blog_command,
# delete_blog_command, view_command, new_command, edit_command, delete_command,
# view_protocol, new_protocol, edit_protocol, delete_protocol, view_type,
# new_type, edit_type, delete_type, view_bench_authority, new_bench_authority,
# edit_bench_authority, delete_bench_authority, view_collection_authority,
# new_collection_authority, edit_collection_authority and
# delete_collection_authority views
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


from matrices.forms import CommandForm
from matrices.forms import BlogForm
from matrices.forms import ProtocolForm
from matrices.forms import TypeForm
from matrices.forms import AuthorityForm
from matrices.forms import CollectionAuthorityForm

from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Command
from matrices.models import Blog
from matrices.models import Authority
from matrices.models import CollectionAuthority

from matrices.routines import get_header_data


HTTP_POST = 'POST'

#
# MAINTENANCE ROUTINES
#

# def view_blog_command(request, blog_id):
# def new_blog_command(request):
# def edit_blog_command(request, blog_id):
# def delete_blog_command(request, blog_id):
#
# def view_command(request, command_id):
# def new_command(request):
# def edit_command(request, command_id):
# def delete_command(request, command_id):
#
# def view_protocol(request, protocol_id):
# def new_protocol(request):
# def edit_protocol(request, protocol_id):
# def delete_protocol(request, protocol_id):
#
# def view_type(request, type_id):
# def new_type(request):
# def edit_type(request, type_id):
# def delete_type(request, type_id):
#
# def view_bench_authority(request, bench_authority_id):
# def new_bench_authority(request):
# def edit_bench_authority(request, bench_authority_id):
# def delete_bench_authority(request, bench_authority_id):
#
# def view_collection_authority(request, collection_authority_id):
# def new_collection_authority(request):
# def edit_collection_authority(request, collection_authority_id):
# def delete_collection_authority(request, collection_authority_id):
#

#
# VIEW A COMMAND TO ACCESS THE BLOGGING ENGINE
#
@login_required
def view_blog_command(request, blog_id):

    data = get_header_data(request.user)

    blog = get_object_or_404(Blog, pk=blog_id)

    if request.user.is_superuser:

        data.update({ 'blog_id': blog_id, 'blog': blog })

        return render(request, 'maintenance/detail_blog_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW COMMAND TO ACCESS THE BLOGGING ENGINE
#
@login_required
def new_blog_command(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = BlogForm(request.POST)

            if form.is_valid:

                blog = form.save(commit=False)

                blog.set_owner(request.user)

                blog.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = BlogForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_blog_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT A COMMAND TO ACCESS THE BLOGGING ENGINE
#
@login_required
def edit_blog_command(request, blog_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        blog = get_object_or_404(Blog, pk=blog_id)

        if request.method == HTTP_POST:

            form = BlogForm(request.POST, instance=blog)

            if form.is_valid:

                blog = form.save(commit=False)

                blog.set_owner(request.user)

                blog.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'blog': blog })

        else:

            form = BlogForm(instance=blog)

            data.update({ 'form': form, 'blog': blog })

        return render(request, 'maintenance/edit_blog_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A COMMAND TO ACCESS THE BLOGGING ENGINE
#
@login_required
def delete_blog_command(request, blog_id):

    if request.user.is_superuser:

        blog = get_object_or_404(Blog, pk=blog_id)

        blog.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# VIEW AN OMERO API COMMAND
#
@login_required
def view_command(request, command_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        command = get_object_or_404(Command, pk=command_id)

        data.update({ 'command_id': command_id, 'command': command })

        return render(request, 'maintenance/detail_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW OMERO API COMMAND
#
@login_required
def new_command(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = CommandForm(request.POST)

            if form.is_valid:

                command = form.save(commit=False)

                command.set_owner(request.user)

                command.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = CommandForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT AN OMERO API COMMAND
#
@login_required
def edit_command(request, command_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        command = get_object_or_404(Command, pk=command_id)

        if request.method == HTTP_POST:

            form = CommandForm(request.POST, instance=command)

            if form.is_valid:

                command = form.save(commit=False)

                command.set_owner(request.user)

                command.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'command': command })

        else:

            form = CommandForm(instance=command)

            data.update({ 'form': form, 'command': command })

        return render(request, 'maintenance/edit_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE AN OMERO API COMMAND
#
@login_required
def delete_command(request, command_id):

    if request.user.is_superuser:

        command = get_object_or_404(Command, pk=command_id)

        command.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# VIEW A TRANSMISSION PROTOCOL
#
@login_required
def view_protocol(request, protocol_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        protocol = get_object_or_404(Protocol, pk=protocol_id)

        data.update({ 'protocol_id': protocol_id, 'protocol': protocol })

        return render(request, 'maintenance/detail_protocol.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW TRANSMISSION PROTOCOL
#
@login_required
def new_protocol(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = ProtocolForm(request.POST)

            if form.is_valid:

                protocol = form.save(commit=False)

                protocol.set_owner(request.user)

                protocol.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = ProtocolForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_protocol.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT A TRANSMISSION PROTOCOL
#
@login_required
def edit_protocol(request, protocol_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        protocol = get_object_or_404(Protocol, pk=protocol_id)

        if request.method == HTTP_POST:

            form = ProtocolForm(request.POST, instance=protocol)

            if form.is_valid:

                protocol = form.save(commit=False)

                protocol.set_owner(request.user)

                protocol.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'protocol': protocol })

        else:

            form = ProtocolForm(instance=protocol)

            data.update({ 'form': form, 'protocol': protocol })

        return render(request, 'maintenance/edit_protocol.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A TRANSMISSION PROTOCOL
#
@login_required
def delete_protocol(request, protocol_id):

    if request.user.is_superuser:

        protocol = get_object_or_404(Protocol, pk=protocol_id)

        protocol.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# VIEW A TYPE OF SERVER
#
@login_required
def view_type(request, type_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        type = get_object_or_404(Type, pk=type_id)

        data.update({ 'type_id': type_id, 'type': type })

        return render(request, 'maintenance/detail_type.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW TYPE OF SERVER
#
@login_required
def new_type(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = TypeForm(request.POST)

            if form.is_valid:

                type = form.save(commit=False)

                type.set_owner(request.user)

                type.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = TypeForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_type.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT A TYPE OF SERVER
#
@login_required
def edit_type(request, type_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        type = get_object_or_404(Type, pk=type_id)

        if request.method == HTTP_POST:

            form = TypeForm(request.POST, instance=type)

            if form.is_valid:

                type = form.save(commit=False)

                type.set_owner(request.user)

                type.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'type': type })

        else:

            form = TypeForm(instance=type)

            data.update({ 'form': form, 'type': type })

        return render(request, 'maintenance/edit_type.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A TYPE OF SERVER
#
@login_required
def delete_type(request, type_id):

    if request.user.is_superuser:

        type = get_object_or_404(Type, pk=type_id)

        type.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# VIEW A BENCH AUTHORITY
#
@login_required
def view_bench_authority(request, bench_authority_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        authority = get_object_or_404(Authority, pk=bench_authority_id)

        data.update({ 'bench_authority_id': bench_authority_id, 'authority': authority })

        return render(request, 'maintenance/detail_bench_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW BENCH AUTHORITY
#
@login_required
def new_bench_authority(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = AuthorityForm(request.POST)

            if form.is_valid:

                authority = form.save(commit=False)

                authority.set_owner(request.user)

                authority.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = AuthorityForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_bench_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT A BENCH AUTHORITY
#
@login_required
def edit_bench_authority(request, bench_authority_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        authority = get_object_or_404(Authority, pk=bench_authority_id)

        if request.method == HTTP_POST:

            form = AuthorityForm(request.POST, instance=authority)

            if form.is_valid:

                authority = form.save(commit=False)

                authority.set_owner(request.user)

                authority.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'authority': authority })

        else:

            form = AuthorityForm(instance=authority)

            data.update({ 'form': form, 'authority': authority })

        return render(request, 'maintenance/edit_bench_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A BENCH AUTHORITY
#
@login_required
def delete_bench_authority(request, bench_authority_id):

    if request.user.is_superuser:

        authority = get_object_or_404(Authority, pk=bench_authority_id)

        authority.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# VIEW A COLLECTION AUTHORITY
#
@login_required
def view_collection_authority(request, collection_authority_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        collection_authority = get_object_or_404(CollectionAuthority, pk=collection_authority_id)

        data.update({ 'collection_authority_id': collection_authority_id, 'collection_authority': collection_authority })

        return render(request, 'maintenance/detail_collection_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# ADD A NEW COLLECTION AUTHORITY
#
@login_required
def new_collection_authority(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = CollectionAuthorityForm(request.POST)

            if form.is_valid:

                collection_authority = form.save(commit=False)

                collection_authority.set_owner(request.user)

                collection_authority.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form })

        else:

            form = CollectionAuthorityForm()

            data.update({ 'form': form })

        return render(request, 'maintenance/new_collection_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# EDIT A COLLECTION AUTHORITY
#
@login_required
def edit_collection_authority(request, collection_authority_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        collection_authority = get_object_or_404(CollectionAuthority, pk=collection_authority_id)

        if request.method == HTTP_POST:

            form = CollectionAuthorityForm(request.POST, instance=collection_authority)

            if form.is_valid:

                collection_authority = form.save(commit=False)

                collection_authority.set_owner(request.user)

                collection_authority.save()

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, "Error")

                data.update({ 'form': form, 'collection_authority': collection_authority })

        else:

            form = CollectionAuthorityForm(instance=collection_authority)

            data.update({ 'form': form, 'collection_authority': collection_authority })

        return render(request, 'maintenance/edit_collection_authority.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))


#
# DELETE A COLLECTION AUTHORITY
#
@login_required
def delete_collection_authority(request, collection_authority_id):

    if request.user.is_superuser:

        collection_authority = get_object_or_404(CollectionAuthority, pk=collection_authority_id)

        collection_authority.delete()

        return HttpResponseRedirect(reverse('maintenance', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
