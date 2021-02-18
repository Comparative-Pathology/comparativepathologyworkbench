from django.contrib import admin

# Register your models here.

from .models import Type
from .models import Protocol
from .models import Command
from .models import Blog
from .models import Credential
from .models import Authority
from .models import CollectionAuthority

admin.site.register(Type)
admin.site.register(Protocol)
admin.site.register(Command)
admin.site.register(Blog)
admin.site.register(Credential)
admin.site.register(Authority)
admin.site.register(CollectionAuthority)
