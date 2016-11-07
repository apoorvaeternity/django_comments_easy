from django import template
from django.template.loader import render_to_string
from ..forms import *
from ..models import CommentsEasy

register = template.Library()


@register.simple_tag(name="render_comment_form", takes_context=True)
def render_comment_form(context, postid):
    request = context["request"]
    return render_to_string("django_commentseasy/commentform.html", {"postid": postid, "form": CommentForm},
                            request=request)


@register.simple_tag(name="render_comment_list", takes_context=True)
def render_comment_list(context, postid):
    com = {'comments': CommentsEasy.objects.filter(postid=postid)}
    request = context["request"]
    return render_to_string("django_commentseasy/commentview.html", com, request=request)


@register.simple_tag(name="get_comment_count")
def get_comment_count(postid):
    count = CommentsEasy.objects.filter(postid=postid).count()
    return count
