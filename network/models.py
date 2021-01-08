from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.urls import reverse


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

    def get_absolute_url(self):
	    return reverse('user-detail', args=[str(self.id)])


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    likes = models.ManyToManyField(User, default=None, related_name="liked")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
	    ordering = ["-timestamp"]

    def serialize(self):
        return {
            "user": self.user.username,
            "id": self.id,
            "content": self.content,
            "likes": [user.username for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
