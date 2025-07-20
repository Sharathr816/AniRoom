from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    pic = models.ImageField(upload_to = 'Avatars/')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username