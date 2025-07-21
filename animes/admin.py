from django.contrib import admin
from .models import Room
from .models import Content
from .models import ChatMsg
from .models import JoinedRooms

# Register your models here.
admin.site.register(Room)
admin.site.register(Content)
admin.site.register(ChatMsg)
admin.site.register(JoinedRooms)