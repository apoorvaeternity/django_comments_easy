from django.shortcuts import render
from .forms import *
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings

# Create your views here.


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
        if settings.ANONYMOUS_ALLOWED:
            new_comment.author = None
        else:
            new_comment.author = 10
        new_comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
