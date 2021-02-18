from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _


from matrices.models import Type


class TypeForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = ('name', )

