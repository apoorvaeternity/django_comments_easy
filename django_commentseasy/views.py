from django.shortcuts import render
from .forms import CommentForm
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from .models import Comments, Likes
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class Testuser(generic.View):
    @staticmethod
    def get(request):
        return render(request, 'django_commentseasy/testuser.html')

    def post( request):
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

        else:l
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
        new_comment = form.save(commit=False)
        if form.is_valid():
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
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        ctx = {'post_id': new_comment.post_id}
        new_comment.save()
        return HttpResponse(render_to_string("django_commentseasy/render_comment_data.html", ctx, request=request))


class CommentLike(View):
    @staticmethod
    def post(request):
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
        post = {'post_id': Comments.objects.get(pk=request.POST["comment_id"]).post_id}
        return HttpResponse(render_to_string("django_commentseasy/render_comment_data.html", post, request=request))


class CommentRemove(View):
    @staticmethod
    def post(request):
        post = {}
        if Comments.objects.filter(id=request.POST["comment_id"], author=request.user).exists():
            ob = Comments.objects.get(id=request.POST["comment_id"], author=request.user)
            post = {'post_id': Comments.objects.get(pk=request.POST["comment_id"]).post_id}
            ob.delete()
        return HttpResponse(render_to_string("django_commentseasy/render_comment_data.html", post, request=request))
