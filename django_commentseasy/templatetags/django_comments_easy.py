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
    com = {'comments': CommentsEasy.objects.filter(postid=postid).order_by("-id")}
    request = context["request"]
    return render_to_string("django_commentseasy/commentviewer.html", com, request=request)


@register.simple_tag(name="render_comment_box", takes_context=True)
def render_comment_box(context,postid):
    request = context["request"]
    return render_to_string("django_commentseasy/commentbox.html", postid, request=request)

@register.simple_tag(name="get_comment_count")
def get_comment_count(postid):
    count = CommentsEasy.objects.filter(postid=int(postid)).count()
    return count

"""
@register.simple_tag(name="get_comment_upvotes")
def get_comment_upvotes(commentid):
    upvotes = CommentsEasy.objects.get(pk=commentid).upvotes
    return upvotes


@register.simple_tag(name="get_comment_downvotes")
def get_comment_downvotes(commentid):
    downvotes = CommentsEasy.objects.get(pk=commentid).downvotes
    return downvotes
"""
@register.simple_tag(name="get_comment_likes")
def get_comment_likes(commentid):
    total_likes = CommentsEasy.objects.get(pk=commentid).total_likes
    return total_likes


@register.simple_tag(name="render_like_button",takes_context=True)
def render_like_button(context,comment_id):
    request = context["request"]
    state=0
    if(Likes.objects.filter(comment=comment_id,user=request.user).exists()==False):
        state=0
    elif Likes.objects.get(comment=comment_id,user=request.user).liked==0:
        state=0
    else:
        state=1
    return render_to_string("django_commentseasy/likebutton.html", {"state": state,"comment":comment_id},
                            request=request)

@register.simple_tag(name="render_remove_button",takes_context=True)
def render_remove_button(context,comment_id):
    request = context["request"]
    my_comment=False
    if CommentsEasy.objects.filter(id=comment_id,author=request.user).exists():
        my_comment=True
    else:
        my_comment=False
    return render_to_string("django_commentseasy/removebutton.html", {"my_comment": my_comment, "comment": comment_id},
                            request=request)



