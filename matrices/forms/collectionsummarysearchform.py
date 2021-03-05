from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import CollectionSummary
from matrices.models import CollectionAuthority


class CollectionSummarySearchForm(forms.ModelForm):
    title = forms.CharField(max_length=20, required=False)
    description = forms.CharField(max_length=20, required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    authority = forms.ModelChoiceField(queryset=CollectionAuthority.objects.all(), required=False)

    class Meta:
        model = CollectionSummary
        fields = ('title',
                'description',
                'owner',
                'authority',
                )
