from django.conf.urls import url

from . import views

app_name = 'django_commentseasy'

urlpatterns = [
    url(r'testuser', views.Testuser.as_view(), name='testuser'),
    url(r'like', views.CommentOperations.like_comment, name='like_comment'),
    url(r'remove', views.CommentOperations.remove_comment, name='remove_comment'),
    url(r'commentform', views.CommentFormView.as_view(), name='comment_form'),
    url(r'^index', views.indexview, name='indexview'),
    ]
