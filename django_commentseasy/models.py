from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Comments(models.Model):

    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post_id = models.IntegerField()
    total_likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, null=True)
    parent_comment = models.ForeignKey("Comments", null=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return str(self.id)


class Likes(models.Model):

    user = models.ForeignKey(User, default=0)
    comment = models.ForeignKey("Comments", default=0)
    liked = models.IntegerField(default=0)
