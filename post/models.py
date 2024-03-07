from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} // {self.slug}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def post_count(self):
        return self.ppostlike.all().count()

    def can_like(self, user):
        can_like = user.upostlike.filter(post=self)
        if can_like.exists():
            return True
        return False

    class Meta:
        ordering = ('created_at',)



class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upostlike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ppostlike')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'