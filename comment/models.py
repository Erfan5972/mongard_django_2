from django.db import models
from django.contrib.auth.models import User
from post.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    reply_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='rcomments')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.is_reply} - {self.body[:30]}"