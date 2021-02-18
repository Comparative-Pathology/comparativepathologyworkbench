from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import Matrix
from matrices.models import Authority
from matrices.models import Authorisation


class AuthorisationForm(forms.ModelForm):

    matrix = forms.ModelChoiceField(queryset=Matrix.objects.all(), label=_('Bench'))
    permitted = forms.ModelChoiceField(queryset=User.objects.all())
    authority = forms.ModelChoiceField(queryset=Authority.objects.all())

    class Meta:
        model = Authorisation
        fields = ('matrix', 'permitted', 'authority', )

