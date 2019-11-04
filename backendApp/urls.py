from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from capstone.models import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('capstone.urls')),
]