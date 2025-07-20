from django.contrib import admin
from django.contrib.auth.models import User #in-built in django
from .models import profile

# Register your models here.
admin.site.register(profile)