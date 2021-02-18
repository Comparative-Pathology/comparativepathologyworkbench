from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import Type
from matrices.models import Server


class ServerForm(forms.ModelForm):

    class Meta:
        model = Server
        fields = ('name', 'url_server', 'uid', 'pwd', 'type')
        widgets = {
            'pwd': forms.PasswordInput(),
        }
        type = forms.ModelChoiceField(queryset=Type.objects.all())

