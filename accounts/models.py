from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unfollow')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follow {self.to_user}'