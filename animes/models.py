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

