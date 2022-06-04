from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    subscribers = models.IntegerField(default=0)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True
    )

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=140)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)