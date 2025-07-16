from django.contrib import admin
from .models import Room
from .models import Content
from .models import ChatMsg

# Register your models here.
admin.site.register(Room)
admin.site.register(Content)
admin.site.register(ChatMsg)