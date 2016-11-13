from django import forms
from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentsEasy
        fields = ('comment',)
        widgets = {
            "comment": forms.Textarea(attrs={"style": "resize:none;", "placeholder": "Write a comment...","cols":"10","rows":"4"})}


