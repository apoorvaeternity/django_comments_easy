from django import template
from django.template.loader import render_to_string
from ..forms import CommentForm
from ..models import Comments, Likes
from django_commentseasy.templatetags import *


register = template.Library()




@register.simple_tag(name="bootstrap_files")
def bootstrap_files():
    return render_to_string("django_commentseasy/bootstrap_files.html")


@register.simple_tag(name="render_comment_form", takes_context=True)
def render_comment_form(context, post_id):
    request = context["request"]
    return render_to_string("django_commentseasy/comment_form.html", {"post_id": post_id, "form": CommentForm},
                            request=request)


@register.simple_tag(name="render_reply_form", takes_context=True)
def render_reply_form(context, comment_id):
    request = context["request"]
    return render_to_string("django_commentseasy/reply_form.html", {"comment_id": comment_id, "form": CommentForm},
                            request=request)


@register.simple_tag(name="render_comment_list", takes_context=True)
def render_comment_list(context, post_id):
    comments = {'comments': Comments.objects.filter(post_id=post_id, parent_comment=None).order_by("id")}
    request = context["request"]
    return render_to_string("django_commentseasy/comment_viewer.html", comments, request=request)


@register.simple_tag(name="render_reply_list", takes_context=True)
def render_reply_list(context, comment_id):
    comments = {'comments': Comments.objects.filter(parent_comment=comment_id).order_by("id")}
    request = context["request"]
    return render_to_string("django_commentseasy/reply_viewer.html", comments, request=request)


@register.simple_tag(name="render_comment_box", takes_context=True)
def render_comment_box(context, post_id):
    request = context["request"]
    post={'post_id':post_id}
    return render_to_string("django_commentseasy/comment_box.html", post, request=request)


@register.simple_tag(name="get_comment_count")
def get_comment_count(post_id):
    count = Comments.objects.filter(post_id=post_id).count()
    return count


@register.simple_tag(name="get_reply_count")
def get_reply_count(comment_id):
    count = Comments.objects.filter(parent_comment=comment_id).count()
    return count


@register.simple_tag(name="get_comment_likes")
def get_comment_likes(comment_id):
    total_likes = Comments.objects.get(pk=comment_id).total_likes
    return total_likes


@register.simple_tag(name="render_like_button", takes_context=True)
def render_like_button(context, comment_id):
    request = context["request"]
    if not request.user.is_authenticated():
        state = -1
    elif Likes.objects.filter(comment=comment_id, user=request.user).exists() is False:
        state = 0
    elif Likes.objects.get(comment=comment_id, user=request.user).liked == 0:
        state = 0
    else:
        state = 1
    return render_to_string("django_commentseasy/like_button.html", {"state": state, "comment": comment_id},
                            request=request)


@register.simple_tag(name="render_remove_button", takes_context=True)
def render_remove_button(context, comment_id):
    request = context["request"]
    if not request.user.is_authenticated():
        my_comment = False
    elif Comments.objects.filter(id=comment_id, author=request.user).exists():
        my_comment = True
    else:
        my_comment = False
    return render_to_string("django_commentseasy/remove_button.html", {"my_comment": my_comment, "comment": comment_id},
                            request=request)
