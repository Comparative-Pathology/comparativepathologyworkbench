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


from matrices.forms import SignUpForm
from matrices.tokens import account_activation_token


HTTP_POST = 'POST'


#
# SIGNUP VIEW ROUTINES
#
# def signup(request):
# def account_activation_sent(request):
# def activate(request, uidb64, token):
#

#
# VIEWS FOR SIGNUP
#
def signup(request):

    if request.method == HTTP_POST:

        form = SignUpForm(request.POST)

        if form.is_valid:

            user = form.save(commit=False)

            user.is_active = False

            user.save()

            current_site = get_current_site(request)

            subject = 'Activate Your Comparative Pathology Workbench Account'
            
            message = render_to_string('user/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)

            return redirect('account_activation_sent')

    else:

        form = SignUpForm()

    return render(request, 'user/signup.html', {'form': form})


#
# ACCOUNT ACTIVATION
#
def account_activation_sent(request):

    return render(request, 'user/account_activation_sent.html')


#
# ACCOUNT ACTIVATE
#
def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        
        return HttpResponseRedirect(reverse('home', args=()))                        

    else:
        
        return render(request, 'user/account_activation_invalid.html')


