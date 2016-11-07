from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CommentsEasy(models.Model):
    def __str__(self):  
        return str(self.id)
    comment = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
    postid = models.IntegerField()
    likes = models.IntegerField(default=0)
    author = models.IntegerField(null=True)
