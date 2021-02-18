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


NO_CREDENTIALS = ''


#
# EBI VIEW ROUTINES
#
# def show_ebi_server(request, server_id):
# def show_ebi_widget(request, server_id, experiment_id):
#

#
# BROWSE THE EBI SERVER
#
@login_required()
def show_ebi_server(request, server_id):
    """
    Show the EBI Server
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        server = get_object_or_404(Server, pk=server_id)
        
        if server.is_omero547() or server.is_omero56():
        
            server_data = server.get_ebi_server_json(request)
        
            data.update(server_data)

            return render(request, 'ebi/show_server.html', data)


#
# BROWSE THE EBI SERVER WIDGET
#
@login_required()
def show_ebi_widget(request, server_id, experiment_id):
    """
    Show the EBI widget
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))                        

    else:

        server = get_object_or_404(Server, pk=server_id)
        
        if server.is_omero547() or server.is_omero56():
        
            server_data = server.get_ebi_widget_json(request)
            
            gene = ''
            
            data.update({ 'experimentAccession': experiment_id, 'geneId': gene })
            
            data.update(server_data)

            return render(request, 'ebi/show_widget.html', data)

