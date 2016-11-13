from django.conf.urls import url

from . import views

app_name = 'django_commentseasy'

urlpatterns = [
    url(r'testuser/$', views.Testuser.as_view(), name='testuser'),
    url(r'like/(?P<commentid>\d+)/$', views.CommentOperations.likecomment, name='likecomment'),
    url(r'remove/(?P<commentid>\d+)/$', views.CommentOperations.removecomment, name='removecomment'),
    #url(r'downvote/(?P<commentid>\d+)/$', views.CommentOperations.downvotecomment, name='downvotecomment'),
    url(r'commentform/$', views.CommentFormView.as_view(), name='commentform'),
    url(r'^index/$', views.indexview, name='indexview'),
    ]