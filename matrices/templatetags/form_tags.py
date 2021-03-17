#!/usr/bin/python3
###!
# \file         form_tags.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# Form tags
###
from django import template

register = template.Library()


@register.filter
def field_type(bound_field):

    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):

    css_class = ''

    if bound_field.form.is_bound:

        if bound_field.errors:

            css_class = 'is-invalid'

        elif field_type(bound_field) != 'PasswordInput':

            css_class = 'is-valid'

    return 'form-control {}'.format(css_class)


@register.simple_tag
def model_name(value):
    '''
    Django template filter which returns the verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name.title()


@register.simple_tag
def model_name_plural(value):
    '''
    Django template filter which returns the plural verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name_plural.title()


@register.simple_tag
def field_name(value, field):
    '''
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.get_field(field).verbose_name.title()
