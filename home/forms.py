from django import forms
from post.models import Post


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']