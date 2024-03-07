from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'body', 'created_at']
    raw_id_fields = ['user', 'post', 'reply_comment']