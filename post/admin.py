from django.contrib import admin
from . models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'body',
                    'slug')
    search_fields = ('slug',)
    list_filter = ('updated_at',)
    prepopulated_fields = {'slug': ('body',)}


admin.site.register(Post, PostAdmin)