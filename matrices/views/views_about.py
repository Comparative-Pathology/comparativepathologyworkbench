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


from matrices.routines import get_header_data


#
# STATIC VIEW ROUTINES
#
# def about(request):
# def people(request):
# def howto(request):
#

#
# ABOUT VIEW
#
def about(request):

    data = get_header_data(request.user)

    return render(request, 'about/about.html', data)


#
# PEOPLE VIEW
#
def people(request):

    data = get_header_data(request.user)

    return render(request, 'about/people.html', data)


#
# HOW TO VIEW
#
def howto(request):

    data = get_header_data(request.user)

    return render(request, 'about/howto.html', data)

