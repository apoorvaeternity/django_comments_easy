from django.shortcuts import render
from .forms import CommentForm
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Comments, Likes
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


class Testuser(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'django_commentseasy/testuser.html')

    def post(self, request, *args, **kwargs):
        user = User.objects.create_user(username=request.POST["user"],
                                        email=request.POST["email"],
                                        password=request.POST["pass"])
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
    template_name = 'django_commentseasy/comment_form.html'

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            if request.user.is_anonymous and request.POST["comment_type"] == "parent":
                new_comment.post_id = request.POST['post_id']
                new_comment.author = None
            elif request.user.is_anonymous and request.POST["comment_type"] == "child":
                new_comment.post_id = Comments.objects.get(id=request.POST['comment_id']).post_id
                new_comment.author = None
                new_comment.parent_comment = Comments.objects.get(id=request.POST['comment_id'])
            elif request.POST["comment_type"] == "parent":
                new_comment.post_id = request.POST['post_id']
                new_comment.author = request.user
            elif request.POST["comment_type"] == "child":
                new_comment.post_id = Comments.objects.get(id=request.POST['comment_id']).post_id
                new_comment.author = request.user
                new_comment.parent_comment = Comments.objects.get(id=request.POST['comment_id'])
            new_comment.save()
        else:
            messages.error(request, "Invalid Comment")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CommentOperations(generic.View):
    @login_required(login_url=settings.LOGIN_URL)
    def like_comment(request):
        ob = Comments.objects.get(pk=request.POST["comment_id"])
        if Likes.objects.filter(comment=request.POST["comment_id"], user=request.user).exists() is False:
            likes_ob = Likes.objects.create(comment=ob, user=request.user)
            likes_ob.liked = 1
            ob.total_likes += 1
            ob.save()
            likes_ob.save()
        else:
            likes_ob = Likes.objects.get(comment=ob, user=request.user)
            if likes_ob.liked == 1:
                likes_ob.liked = 0
                ob.total_likes -= 1
                ob.save()
                likes_ob.save()
            else:
                likes_ob.liked = 1
                ob.total_likes += 1
                ob.save()
                likes_ob.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    @login_required(login_url=settings.LOGIN_URL)
    def remove_comment(request):
        if Comments.objects.filter(id=request.POST["comment_id"], author=request.user).exists():
            ob = Comments.objects.get(id=request.POST["comment_id"], author=request.user)
            ob.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
