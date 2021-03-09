"""
    comparativepathologyworkbench URL Configuration
"""
from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include('matrices.urls')),

    path('admin/', admin.site.urls),
]
