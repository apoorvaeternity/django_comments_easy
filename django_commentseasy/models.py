from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CommentsEasy(models.Model):
    class Meta:
        ordering = ('timestamp',)
    def __str__(self):  
        return str(self.id)
    comment = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    postid = models.IntegerField()
    total_likes = models.IntegerField(default=0)
    author = models.ForeignKey(User,default=0)
    parentcomment = models.IntegerField(null=True)

class Likes(models.Model):
    user = models.ForeignKey(User,default=0)
    comment = models.ForeignKey(CommentsEasy,default=0)
    liked = models.IntegerField(default=0)


