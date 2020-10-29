from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Server
from matrices.models import Command
from matrices.models import Command
from matrices.models import Image
from matrices.models import Blog
from matrices.models import Credential
from matrices.models import Authority
from matrices.models import Authorisation

from django.forms.widgets import Select
from django.forms.widgets import SelectMultiple
from django.forms.widgets import RadioSelect


class CellForm(forms.ModelForm):

    class Meta:
        model = Cell
        fields = ('title', 'description', 'image')

    def __init__(self, user_id=None, image_id=None, *args, **kwargs):
        super(CellForm, self).__init__(*args, **kwargs)

        querysetActive = Image.objects.none()
        querysetSelected = Image.objects.none()
    
        if image_id is not None:
            querysetSelected = Image.objects.filter(owner=user_id).filter(id=image_id)
            
        if user_id is not None:
            querysetActive = Image.objects.filter(owner=user_id).filter(active=True)
        
        querysetCombined = querysetActive | querysetSelected
            
        self.fields['image'] = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=querysetCombined, empty_label=None)
        self.fields['image'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        """
        Shows an image with the label
        """
        image_id = conditional_escape(obj.identifier)
        viewer_url = conditional_escape(obj.viewer_url)
        birdseye_url = conditional_escape(obj.birdseye_url)
        name = conditional_escape(obj.name)
        
        label = """%s<a href="%s" target="_blank"><img  style="width:256px; height:256px; float: left" title="%s" src="%s" ></a>""" % (name, viewer_url, name, birdseye_url)
        
        return mark_safe(label)


class HeaderForm(forms.ModelForm):

    class Meta:
        model = Cell
        fields = ('title', 'description')

        
class NewMatrixForm(forms.ModelForm):
    columns = forms.IntegerField(initial=1)
    rows = forms.IntegerField(initial=1)

    class Meta:
        model = Matrix
        fields = ('title', 'description', 'height', 'width' )


class MatrixForm(forms.ModelForm):

    class Meta:
        model = Matrix
        fields = ('title', 'description', 'height', 'width' )


class CommandForm(forms.ModelForm):

    class Meta:
        model = Command
        fields = ('name', 'type', 'application', 'preamble', 'postamble', 'protocol')
        protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())
        type = forms.ModelChoiceField(queryset=Type.objects.all())


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('name', 'protocol', 'url_blog', 'application', 'preamble', 'postamble', )
        protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())


class CredentialForm(forms.ModelForm):

    class Meta:
        model = Credential
        fields = ('username', 'wordpress', 'apppwd', )


class ServerForm(forms.ModelForm):

    class Meta:
        model = Server
        fields = ('name', 'url_server', 'uid', 'pwd', 'type')
        widgets = {
            'pwd': forms.PasswordInput(),
        }
        type = forms.ModelChoiceField(queryset=Type.objects.all())


class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        fields = ('name', )


class TypeForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = ('name', )


class AuthorityForm(forms.ModelForm):

    class Meta:
        model = Authority
        fields = ('name', )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Supply a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Supply a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'email', )


class CommentForm(forms.Form):

    comment = forms.CharField(max_length=4095, required=True, help_text='Required.')


class AuthorisationForm(forms.ModelForm):

    matrix = forms.ModelChoiceField(queryset=Matrix.objects.all())
    permitted = forms.ModelChoiceField(queryset=User.objects.all())
    authority = forms.ModelChoiceField(queryset=Authority.objects.all())

    class Meta:
        model = Authorisation
        fields = '__all__'
