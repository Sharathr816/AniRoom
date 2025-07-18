from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.TextField()
    tag = models.CharField(max_length = 255, blank = True)
    image = models.ImageField(upload_to = 'anime_images/')
    uploaded_by = models.ForeignKey(User, on_delete = models.CASCADE)#if user deleted, uploads also deleted
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):#for 'title' view in admin panel(cause no need of encrypted view)
        return self.title

class Content(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    img = models.ImageField(upload_to = 'room_imgs/')
    vid = models.FileField(upload_to = 'room_vids_musics/') #check does it allow multi file upload at once
    mus = models.FileField(upload_to = 'room_musics/')




class ChatMsg(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    chats = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} - {self.chats[:30]}"




