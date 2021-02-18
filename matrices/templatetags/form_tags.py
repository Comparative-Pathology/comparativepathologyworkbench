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