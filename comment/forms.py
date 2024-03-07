from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReplyCommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']