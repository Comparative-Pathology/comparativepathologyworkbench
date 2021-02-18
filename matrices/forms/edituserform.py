from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Supply a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'email', )

