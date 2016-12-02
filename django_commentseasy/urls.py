from django.conf.urls import url

from . import views

app_name = 'django_commentseasy'

urlpatterns = [
    url(r'testuser', views.Testuser.as_view(), name='testuser'),
    url(r'like', views.CommentLike.as_view(), name='like_comment'),
    url(r'remove', views.CommentRemove.as_view(), name='remove_comment'),
    url(r'commentform', views.CommentFormView.as_view(), name='comment_form'),
    url(r'^index', views.indexview, name='indexview'),
    ]
