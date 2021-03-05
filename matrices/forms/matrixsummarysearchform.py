from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import MatrixSummary
from matrices.models import Authority


class MatrixSummarySearchForm(forms.ModelForm):
    title = forms.CharField(max_length=20, required=False)
    description = forms.CharField(max_length=20, required=False)
    created_before = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
    created_after = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
    modified_before = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
    modified_after = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    authority = forms.ModelChoiceField(queryset=Authority.objects.all(), required=False)

    class Meta:
        model = MatrixSummary
        fields = ('title',
                'description',
                'owner',
                'authority',
                'created_before',
                'created_after',
                'modified_before',
                'modified_after',
                )
