from django.conf.urls import url

from . import views

app_name = 'django_commentseasy'

urlpatterns = [
    url(r'commentform/$', views.CommentFormView.as_view(), name='commentform'),
    url(r'^index/$', views.indexview, name='indexview'),
    ]