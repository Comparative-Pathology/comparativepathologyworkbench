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

from matrices.forms import ServerForm

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Server
from matrices.models import Command
from matrices.models import Image
from matrices.models import Blog
from matrices.models import Credential
from matrices.models import Collection
from matrices.models import Authority
from matrices.models import CollectionAuthority
from matrices.models import Authorisation
from matrices.models import CollectionAuthorisation

from matrices.routines import AESCipher
from matrices.routines import authorisation_list_select_related_bench_by_user
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import bench_list_by_user
from matrices.routines import bench_list_not_by_user
from matrices.routines import get_header_data


WORDPRESS_SUCCESS = 'Success!'

HTTP_POST = 'POST'

NO_CREDENTIALS = ''


#
# THE HOST VIEW ROUTINES
#
# def home(request):
# def view_server(request, server_id):
# def new_server(request):
# def edit_server(request, server_id):
# def delete_server(request, server_id):
# def authorisation(request):
# def maintenance(request):
# def index_matrix(request):
# def list_imaging_hosts(request):
# def list_image_cart(request):
# def index_collection(request):
# def list_bench_authorisation(request):
# def list_my_bench_authorisation(request):
# def list_my_bench_bench_authorisation(request, matrix_id, user_id):
# def list_bench_bench_authorisation(request, matrix_id):
# def list_user_bench_bench_authorisation(request, user_id):
# def list_collection_authorisation(request):
# def list_my_collection_authorisation(request):
# def list_my_collection_collection_authorisation(request, collection_id, user_id):
# def list_collection_collection_authorisation(request, collection_id):
# def list_user_collection_collection_authorisation(request, user_id):
#

#
# HOME VIEW
#
def home(request):

    data = get_header_data(request.user)
    
    return render(request, 'host/home.html', data)


#
# VIEW A NEW IMAGE SERVER DETAILS
#
@login_required
def view_server(request, server_id):

    data = get_header_data(request.user)
    
    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        server = get_object_or_404(Server, pk=server_id)
    
        owner = get_object_or_404(User, pk=server.owner_id)

        cipher = AESCipher(config('NOT_EMAIL_HOST_PASSWORD'))
    
        decryptedPwd = cipher.decrypt(server.pwd)

        data.update({ 'owner': owner, 'server': server })

        return render(request, 'host/detail_server.html', data)

    
#
# ADD A NEW IMAGE SERVER
#
@login_required
def new_server(request):

    data = get_header_data(request.user)
    
    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        if request.method == HTTP_POST:
    
            form = ServerForm(request.POST)
        
            if form.is_valid:
        
                server = form.save(commit=False)

                server.set_owner(request.user)

                cipher = AESCipher(config('NOT_EMAIL_HOST_PASSWORD'))
                
                encryptedPwd = cipher.encrypt(server.pwd).decode()

                server.set_pwd(encryptedPwd)

                server.save()

                return HttpResponseRedirect(reverse('list_imaging_hosts', args=()))                        

            else:

                messages.error(request, "Error")

                data.update({ 'form': form,  })

        else:

            form = ServerForm()

            data.update({ 'form': form,  })

        return render(request, 'host/new_server.html', data)

    
#
# EDIT AN IMAGE SERVER
#
@login_required
def edit_server(request, server_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        server = get_object_or_404(Server, pk=server_id)
    
        if server.is_owned_by(request.user) or request.user.is_superuser:

            if request.method == HTTP_POST:
    
                form = ServerForm(request.POST, instance=server)
            
                if form.is_valid:
            
                    server = form.save(commit=False)

                    cipher = AESCipher(config('NOT_EMAIL_HOST_PASSWORD'))
                    
                    encryptedPwd = cipher.encrypt(server.pwd).decode()

                    server.set_pwd(encryptedPwd)
                
                    server.set_owner(request.user)

                    server.save()
                
                    return HttpResponseRedirect(reverse('list_imaging_hosts', args=()))                        

                else:
            
                    messages.error(request, "Error")
    
                    data.update({ 'form': form, 'server': server })
            
            else:
    
                form = ServerForm(instance=server)
            
                data.update({ 'form': form, 'server': server })

            return render(request, 'host/edit_server.html', data)
    
        else:

            return HttpResponseRedirect(reverse('home', args=()))                        


#
# DELETE AN IMAGE SERVER
#
@login_required
def delete_server(request, server_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        server = get_object_or_404(Server, pk=server_id)
    
        if server.is_owned_by(request.user) or request.user.is_superuser:

            server.delete()
    
            return HttpResponseRedirect(reverse('list_imaging_hosts', args=()))                        

        else:

            return HttpResponseRedirect(reverse('home', args=()))                        
    

#
# SHOW THE AUTHORISATION PAGE
#
@login_required
def authorisation(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)
    
        user_list = User.objects.all()
        credential_list = Credential.objects.all()

        data.update({ 'user_list': user_list })
        data.update({ 'credential_list': credential_list })

        return render(request, 'host/authorisation.html', data)
    
    else:

        return HttpResponseRedirect(reverse('home', args=()))                        


#
# SHOW THE MAINTENANCE PAGE
#
@login_required
def maintenance(request):
    
    if request.user.is_superuser:

        data = get_header_data(request.user)
    
        type_list = Type.objects.all()
        protocol_list = Protocol.objects.all()
        command_list = Command.objects.all()
        blog_list = Blog.objects.all()
        authority_list = Authority.objects.all()
        collection_authority_list = CollectionAuthority.objects.all()

        data.update({ 'type_list': type_list, 'protocol_list': protocol_list, 'command_list': command_list, 'blog_list': blog_list, 'authority_list': authority_list, 'collection_authority_list': collection_authority_list })
    
        return render(request, 'host/maintenance.html', data)
    
    else:

        return HttpResponseRedirect(reverse('home', args=()))                        


#
# VIEWS FOR ALL MY MATRICES
#
@login_required
def index_matrix(request):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:
    
        my_out_matrix_list = list()
        all_out_matrix_list = list()

        my_out_matrix_list = bench_list_by_user(request.user)

        if request.user.is_superuser:

            all_out_matrix_list = bench_list_not_by_user(request.user)
    
        else:

            matrix_list_1 = bench_list_by_user(request.user)
            matrix_list_2 = authorisation_list_select_related_bench_by_user(request.user)
        
            all_out_matrix_list = matrix_list_1 + matrix_list_2
    
        data.update({ 'my_out_matrix_list': my_out_matrix_list, 'all_out_matrix_list': all_out_matrix_list })

        return render(request, 'host/index.html', data)


#
# LIST SERVERS
#
@login_required
def list_imaging_hosts(request):

    data = get_header_data(request.user)
    
    return render(request, 'host/list_imaging_hosts.html', data)
    

#
# LIST IMAGE BASKET
#
@login_required
def list_image_cart(request):

    data = get_header_data(request.user)

    return render(request, 'host/list_image_cart.html', data)
    

#
# LIST IMAGE COLLECTIONS
#
@login_required
def index_collection(request):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        return render(request, 'host/list_collection.html', data)


#
# LIST ALL PERMISSIONS FOR ALL BENCHES
#
@login_required
def list_bench_authorisation(request):

    data = get_header_data(request.user)
    
    authorisation_list = Authorisation.objects.all()

    text_flag = ' ALL Permissions, ALL Benches'
    matrix_id = ''
    
    data.update({ 'matrix_id': matrix_id, 'text_flag': text_flag, 'authorisation_list': authorisation_list })

    return render(request, 'host/list_bench_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FOR A USERS BENCHES
#
@login_required
def list_my_bench_authorisation(request):

    data = get_header_data(request.user)

    authorisation_list = Authorisation.objects.filter(matrix__owner=request.user)

    text_flag = ' YOUR Bench Permissions'    
    matrix_id = ''

    data.update({ 'matrix_id': matrix_id, 'text_flag': text_flag, 'authorisation_list': authorisation_list })

    return render(request, 'host/list_bench_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FROM A USER FOR A BENCH
#
@login_required
def list_my_bench_bench_authorisation(request, matrix_id, user_id):

    data = get_header_data(request.user)
    
    authorisation_list = Authorisation.objects.filter(matrix__owner=user_id).filter(matrix__id=matrix_id)

    user = get_object_or_404(User, pk=user_id)

    text_flag = "Permissions for Bench CPW:" + format(int(matrix_id), '06d') + " for User " + user.username

    data.update({ 'matrix_id': matrix_id, 'text_flag': text_flag, 'authorisation_list': authorisation_list, 'user_id': user_id })

    return render(request, 'host/list_bench_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FOR A BENCH
#
@login_required
def list_bench_bench_authorisation(request, matrix_id):

    data = get_header_data(request.user)

    authorisation_list = Authorisation.objects.filter(matrix__id=matrix_id)

    text_flag = "Permissions for Bench CPW:" + format(int(matrix_id), '06d')

    data.update({ 'matrix_id': matrix_id, 'text_flag': text_flag, 'authorisation_list': authorisation_list })

    return render(request, 'host/list_bench_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FROM A USER FOR ALL BENCHES
#
@login_required
def list_user_bench_bench_authorisation(request, user_id):

    data = get_header_data(request.user)
    
    authorisation_list = Authorisation.objects.filter(matrix__owner=user_id)

    user = get_object_or_404(User, pk=user_id)

    text_flag = " ALL Bench Permissions for " + user.username
    matrix_id = ''

    data.update({ 'matrix_id': matrix_id, 'text_flag': text_flag, 'authorisation_list': authorisation_list, 'user_id': user_id })

    return render(request, 'host/list_bench_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FOR ALL COLLECTIONS
#
@login_required
def list_collection_authorisation(request):

    data = get_header_data(request.user)

    collection_authorisation_list = CollectionAuthorisation.objects.all()

    text_flag = ' ALL Collection Permissions, ALL Collections'
    collection_id = ''
    
    data.update({ 'collection_id': collection_id, 'text_flag': text_flag, 'collection_authorisation_list': collection_authorisation_list })

    return render(request, 'host/list_collection_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FOR A USERS COLLECTIONS
#
@login_required
def list_my_collection_authorisation(request):

    data = get_header_data(request.user)

    collection_authorisation_list = CollectionAuthorisation.objects.filter(collection__owner=request.user)

    text_flag = ' YOUR Collection Permissions'    
    collection_id = ''

    data.update({ 'collection_id': collection_id, 'text_flag': text_flag, 'collection_authorisation_list': collection_authorisation_list })

    return render(request, 'host/list_collection_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FROM A USER FOR A COLLECTION
#
@login_required
def list_my_collection_collection_authorisation(request, collection_id, user_id):

    data = get_header_data(request.user)

    collection_authorisation_list = CollectionAuthorisation.objects.filter(collection__owner=user_id).filter(collection__id=collection_id)

    user = get_object_or_404(User, pk=user_id)

    text_flag = "Permissions for Collection:" + format(int(collection_id), '06d') + " for User " + user.username

    data.update({ 'collection_id': collection_id, 'user_id': user_id, 'text_flag': text_flag, 'collection_authorisation_list': collection_authorisation_list })

    return render(request, 'host/list_collection_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FOR A COLLECTION
#
@login_required
def list_collection_collection_authorisation(request, collection_id):

    data = get_header_data(request.user)

    collection_authorisation_list = CollectionAuthorisation.objects.filter(collection__id=collection_id)
    
    text_flag = "Permissions for Collection:" + format(int(collection_id), '06d')
    
    data.update({ 'collection_id': collection_id, 'text_flag': text_flag, 'collection_authorisation_list': collection_authorisation_list })

    return render(request, 'host/list_collection_authorisation.html', data)
    

#
# LIST ALL PERMISSIONS FROM A USER FOR ALL COLLECTIONS
#
@login_required
def list_user_collection_collection_authorisation(request, user_id):

    data = get_header_data(request.user)

    collection_authorisation_list = CollectionAuthorisation.objects.filter(matrix__owner=user_id)

    user = get_object_or_404(User, pk=user_id)

    text_flag = " ALL Collection Permissions for " + user.username
    collection_id = ''

    data.update({ 'collection_id': collection_id, 'user_id': user_id, 'text_flag': text_flag, 'collection_authorisation_list': collection_authorisation_list })

    return render(request, 'host/list_collection_authorisation.html', data)
    

