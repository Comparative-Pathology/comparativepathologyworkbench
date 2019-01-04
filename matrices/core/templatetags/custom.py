import re
from django import template
from django.conf import settings


register = template.Library()
numeric_test = re.compile("^\d+$")

	
@register.filter
def index(List, i):
	return List[int(i)]

@register.filter
def entry_num_array(List):
	return range(len(List))

