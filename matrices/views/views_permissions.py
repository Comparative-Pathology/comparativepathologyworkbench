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


from matrices.forms import AuthorisationForm
from matrices.forms import CollectionAuthorisationForm

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

from matrices.routines import collection_authorisation_exists_for_collection_and_permitted
from matrices.routines import authorisation_exists_for_bench_and_permitted
from matrices.routines import credential_exists
from matrices.routines import get_header_data


HTTP_POST = 'POST'


#
# BENCH AND COLLECTION AUTHORISATION ROUTINES
#
# def view_bench_authorisation(request, bench_authorisation_id):
# def new_bench_authorisation(request):
# def new_bench_bench_authorisation(request, matrix_id):
# def edit_bench_authorisation(request, bench_authorisation_id):
# def edit_bench_bench_authorisation(request, matrix_id, bench_authorisation_id):
# def delete_bench_authorisation(request, bench_authorisation_id):
#
# def view_collection_authorisation(request, collection_authorisation_id):
# def new_collection_authorisation(request):
# def new_collection_collection_authorisation(request, collection_id):
# def edit_collection_authorisation(request, collection_authorisation_id):
# def edit_collection_collection_authorisation(request, collection_id, collection_authorisation_id):
# def delete_collection_authorisation(request, collection_authorisation_id):
#

#
# VIEW THE BENCH AUTHORISATION
#
@login_required
def view_bench_authorisation(request, bench_authorisation_id):

    data = get_header_data(request.user)
    
    authorisation = get_object_or_404(Authorisation, pk=bench_authorisation_id)

    data.update({ 'authorisation_id': bench_authorisation_id, 'authorisation': authorisation })

    return render(request, 'permissions/detail_bench_authorisation.html', data)


#
# CREATE A NEW BENCH AUTHORISATION
#
@login_required
def new_bench_authorisation(request):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:
        
        next_page = request.POST.get('next', '/')

        form = AuthorisationForm(request.POST)

        if form.is_valid:
        
            authorisation = form.save(commit=False)
            
            if authorisation_exists_for_bench_and_permitted(authorisation.matrix, authorisation.permitted):
            
                authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
                
                if authorisation_old.authority != authorisation.authority:
                
                    authorisation_old.authority = authorisation.authority
                    
                    authorisation_old.save()

            else:
            
                authorisation.save()

            return HttpResponseRedirect(next_page)                        
        
        else:
        
            text_flag = ''

            messages.error(request, "Error")

            data.update({ 'text_flag': text_flag, 'form': form })
            
    else:
    
        text_flag = ''

        form = AuthorisationForm()

        if request.user.is_superuser:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.all())
        
        else:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(owner=request.user))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form })

    return render(request, 'permissions/new_bench_authorisation.html', data)

    
#
# CREATE A NEW BENCH AUTHORISATION FOR A GIVEN BENCH
#
@login_required
def new_bench_bench_authorisation(request, matrix_id):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:
        
        next_page = request.POST.get('next', '/')

        form = AuthorisationForm(request.POST)

        if form.is_valid:
        
            authorisation = form.save(commit=False)
            
            if authorisation_exists_for_bench_and_permitted(authorisation.matrix, authorisation.permitted):
            
                authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
                
                if authorisation_old.authority != authorisation.authority:
                
                    authorisation_old.authority = authorisation.authority
                    
                    authorisation_old.save()

            else:
            
                authorisation.save()

            return HttpResponseRedirect(next_page)                        
        
        else:
        
            messages.error(request, "Error")

            text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
    
            data.update({ 'text_flag': text_flag, 'form': form })
            
    else:
    
        text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
    
        form = AuthorisationForm()

        form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(id=matrix_id))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form })

    return render(request, 'permissions/new_bench_authorisation.html', data)


#
# CREATE A BENCH AUTHORISATION
#
@login_required
def edit_bench_authorisation(request, bench_authorisation_id):

    data = get_header_data(request.user)

    authorisation = get_object_or_404(Authorisation, pk=bench_authorisation_id)
    
    if request.method == HTTP_POST:
    
        next_page = request.POST.get('next', '/')
        
        form = AuthorisationForm(request.POST, instance=authorisation)
            
        if form.is_valid:
            
            authorisation = form.save(commit=False)

            if authorisation_exists_for_bench_and_permitted(authorisation.matrix, authorisation.permitted):
            
                authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
                
                if authorisation_old.authority != authorisation.authority:
                
                    authorisation_old.authority = authorisation.authority
                    
                    authorisation_old.save()

            else:
            
                authorisation.save()

            return HttpResponseRedirect(next_page)                        

        else:
            
            text_flag = ''
    
            messages.error(request, "Error")
    
            data.update({ 'text_flag': text_flag, 'form': form, 'authorisation': authorisation })
            
    else:
    
        text_flag = ''
        
        form = AuthorisationForm(instance=authorisation)

        if request.user.is_superuser:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.all())
        
        else:

            form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(owner=request.user))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
            
        data.update({ 'text_flag': text_flag, 'form': form, 'authorisation': authorisation })

    return render(request, 'permissions/edit_bench_authorisation.html', data)


#
# EDIT A BENCH AUTHORISATION FOR A GIVEN BENCH
#
@login_required
def edit_bench_bench_authorisation(request, matrix_id, bench_authorisation_id):

    data = get_header_data(request.user)

    authorisation = get_object_or_404(Authorisation, pk=bench_authorisation_id)
    
    if request.method == HTTP_POST:
    
        next_page = request.POST.get('next', '/')
        
        form = AuthorisationForm(request.POST, instance=authorisation)
            
        if form.is_valid:
            
            authorisation = form.save(commit=False)

            if authorisation_exists_for_bench_and_permitted(authorisation.matrix, authorisation.permitted):
            
                authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
                
                if authorisation_old.authority != authorisation.authority:
                
                    authorisation_old.authority = authorisation.authority
                    
                    authorisation_old.save()

            else:
            
                authorisation.save()

            return HttpResponseRedirect(next_page)                        

        else:
            
            text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
    
            messages.error(request, "Error")
    
            data.update({ 'text_flag': text_flag, 'form': form, 'authorisation': authorisation })
            
    else:
    
        text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
    
        form = AuthorisationForm(instance=authorisation)

        form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(id=matrix_id))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
            
        data.update({ 'text_flag': text_flag, 'form': form, 'authorisation': authorisation })

    return render(request, 'permissions/edit_bench_authorisation.html', data)


#
# DELETE A BENCH AUTHORISATION
#
@login_required
def delete_bench_authorisation(request, bench_authorisation_id):

    authorisation = get_object_or_404(Authorisation, pk=bench_authorisation_id)
    
    authorisation.delete()
    
    return HttpResponseRedirect(reverse('list_bench_authorisation', args=()))                        


#
# VIEW THE COLLECTION AUTHORISATION
#
@login_required
def view_collection_authorisation(request, collection_authorisation_id):

    data = get_header_data(request.user)

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)

    data.update({ 'collection_authorisation_id': collection_authorisation_id, 'collection_authorisation': collection_authorisation })

    return render(request, 'permissions/detail_collection_authorisation.html', data)


#
# CREATE A NEW COLLECTION AUTHORISATION
#
@login_required
def new_collection_authorisation(request):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:
        
        next_page = request.POST.get('next', '/')

        form = CollectionAuthorisationForm(request.POST)
        
        if form.is_valid:
        
            collection_authorisation = form.save(commit=False)
            
            if collection_authorisation_exists_for_collection_and_permitted(collection_authorisation.collection, collection_authorisation.permitted):
            
                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection_authorisation.collection) & Q(permitted=collection_authorisation.permitted))
                
                if collection_authorisation_old.authority != collection_authorisation.authority:
                
                    collection_authorisation_old.authority = collection_authorisation.authority
                    
                    collection_authorisation_old.save()

            else:
            
                collection_authorisation.save()

            return HttpResponseRedirect(next_page)                        
        
        else:
        
            text_flag = ''

            messages.error(request, "Error")

            data.update({ 'text_flag': text_flag, 'form': form })
            
    else:
    
        text_flag = ''

        form = CollectionAuthorisationForm()

        if request.user.is_superuser:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.all())
        
        else:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(owner=request.user))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form })

    return render(request, 'permissions/new_collection_authorisation.html', data)


#
# CREATE A NEW COLLECTION AUTHORISATION FOR A GIVEN COLLECTION
#
@login_required
def new_collection_collection_authorisation(request, collection_id):

    data = get_header_data(request.user)

    if request.method == HTTP_POST:
        
        next_page = request.POST.get('next', '/')

        form = CollectionAuthorisationForm(request.POST)

        if form.is_valid:
        
            collection_authorisation = form.save(commit=False)
            
            if collection_authorisation_exists_for_collection_and_permitted(collection_authorisation.collection, collection_authorisation.permitted):
            
                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection_authorisation.collection) & Q(permitted=collection_authorisation.permitted))
                
                if collection_authorisation_old.authority != collection_authorisation.authority:
                
                    collection_authorisation_old.authority = collection_authorisation.authority
                    
                    collection_authorisation_old.save()

            else:
            
                collection_authorisation.save()

            return HttpResponseRedirect(next_page)                        
        
        else:
        
            messages.error(request, "Error")

            text_flag = " for Collection: " + format(int(collection_id), '06d')
    
            data.update({ 'text_flag': text_flag, 'form': form })
            
    else:
    
        text_flag = " for Collection: " + format(int(collection_id), '06d')
    
        form = CollectionAuthorisationForm()

        form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(id=collection_id))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

        data.update({ 'text_flag': text_flag, 'form': form })

    return render(request, 'permissions/new_collection_authorisation.html', data)


#
# CREATE A COLLECTION AUTHORISATION
#
@login_required
def edit_collection_authorisation(request, collection_authorisation_id):

    data = get_header_data(request.user)

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)
    
    if request.method == HTTP_POST:
    
        next_page = request.POST.get('next', '/')
        
        form = CollectionAuthorisationForm(request.POST, instance=collection_authorisation)
            
        if form.is_valid:
            
            collection_authorisation = form.save(commit=False)

            if collection_authorisation_exists_for_collection_and_permitted(collection_authorisation.collection, collection_authorisation.permitted):
            
                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection_authorisation.collection) & Q(permitted=collection_authorisation.permitted))
                
                if collection_authorisation_old.authority != collection_authorisation.authority:
                
                    collection_authorisation_old.authority = collection_authorisation.authority
                    
                    collection_authorisation_old.save()

            else:
            
                collection_authorisation.save()

            return HttpResponseRedirect(next_page)                        

        else:
            
            text_flag = ''
    
            messages.error(request, "Error")
    
            data.update({ 'text_flag': text_flag, 'form': form, 'collection_authorisation': collection_authorisation })
            
    else:
    
        text_flag = ''
        
        form = CollectionAuthorisationForm(instance=collection_authorisation)

        if request.user.is_superuser:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.all())
        
        else:

            form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(owner=request.user))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
            
        data.update({ 'text_flag': text_flag, 'form': form, 'collection_authorisation': collection_authorisation })

    return render(request, 'permissions/edit_collection_authorisation.html', data)


#
# EDIT A COLLECTION AUTHORISATION FOR A GIVEN COLLECTION
#
@login_required
def edit_collection_collection_authorisation(request, collection_id, collection_authorisation_id):

    data = get_header_data(request.user)

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)
    
    if request.method == HTTP_POST:
    
        next_page = request.POST.get('next', '/')
        
        form = CollectionAuthorisationForm(request.POST, instance=collection_authorisation)
            
        if form.is_valid:
            
            collection_authorisation = form.save(commit=False)

            if collection_authorisation_exists_for_collection_and_permitted(collection_authorisation.collection, collection_authorisation.permitted):
            
                collection_authorisation_old = CollectionAuthorisation.objects.get(Q(collection=collection_authorisation.collection) & Q(permitted=collection_authorisation.permitted))
                
                if collection_authorisation_old.authority != collection_authorisation.authority:
                
                    collection_authorisation_old.authority = collection_authorisation.authority
                    
                    collection_authorisation_old.save()

            else:
            
                collection_authorisation.save()

            return HttpResponseRedirect(next_page)                        

        else:
            
            text_flag = " for Bench CPW:" + format(int(collection_id), '06d')
    
            messages.error(request, "Error")
    
            data.update({ 'text_flag': text_flag, 'form': form, 'collection_authorisation': collection_authorisation })
            
    else:
    
        text_flag = " for Bench CPW:" + format(int(collection_id), '06d')
    
        form = CollectionAuthorisationForm(instance=collection_authorisation)

        form.fields['collection'] = forms.ModelChoiceField(Collection.objects.filter(id=collection_id))

        form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
            
        data.update({ 'text_flag': text_flag, 'form': form, 'collection_authorisation': collection_authorisation })

    return render(request, 'permissions/edit_collection_authorisation.html', data)


#
# DELETE A COLLECTION AUTHORISATION
#
@login_required
def delete_collection_authorisation(request, collection_authorisation_id):

    collection_authorisation = get_object_or_404(CollectionAuthorisation, pk=collection_authorisation_id)
    
    collection_authorisation.delete()
    
    return HttpResponseRedirect(reverse('list_collection_authorisation', args=()))                        

