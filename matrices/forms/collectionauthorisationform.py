from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import Collection
from matrices.models import CollectionAuthority
from matrices.models import CollectionAuthorisation


class CollectionAuthorisationForm(forms.ModelForm):

    collection = forms.ModelChoiceField(queryset=Collection.objects.all())
    permitted = forms.ModelChoiceField(queryset=User.objects.all())
    collection_authority = forms.ModelChoiceField(queryset=CollectionAuthority.objects.all())

    class Meta:
        model = CollectionAuthorisation
        fields = ('collection', 'permitted', 'collection_authority', )

