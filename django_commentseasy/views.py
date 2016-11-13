from django.shortcuts import render
from .forms import *
from django.views import generic
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login




class Testuser(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request,'django_commentseasy/testuser.html')
    def post(self,request,*args,**kwargs):
        user = User.objects.create_user(username=request.POST["user"],email=request.POST["email"],password=request.POST["pass"])
        user.save()
        username = request.POST["user"]
        password = request.POST["pass"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("http://www.google.com")

        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect("http://www.google.com")


def indexview(request):
    template_name = 'django_commentseasy/check.html'
    return render(request, template_name)


class CommentFormView(generic.edit.FormView):
    form_class = CommentForm
    template_name = 'django_commentseasy/commentform.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        new_comment = form.save(commit=False)
        new_comment.postid = request.POST['postid']
        new_comment.author=request.user
        new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CommentOperations(generic.View):
    @login_required(login_url=settings.LOGIN_URL)
    def likecomment(request, commentid):
        ob = CommentsEasy.objects.get(pk=commentid)
        if(Likes.objects.filter(comment=commentid,user=request.user).exists()==False):
            likes_ob=Likes.objects.create(comment=ob,user=request.user)
            likes_ob.liked=1
            ob.total_likes+=1
            ob.save()
            likes_ob.save()
        else:
            likes_ob = Likes.objects.get(comment=ob, user=request.user)
            if(likes_ob.liked==1):
                likes_ob.liked=0
                ob.total_likes-=1
                ob.save()
                likes_ob.save()
            else:
                likes_ob.liked=1
                ob.total_likes+=1
                ob.save()
                likes_ob.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    @login_required(login_url=settings.LOGIN_URL)
    def removecomment(request, commentid):
        if CommentsEasy.objects.filter(id=commentid, author=request.user).exists():
            ob=CommentsEasy.objects.get(id=commentid, author=request.user)
            ob.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))







