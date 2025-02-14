from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username} - Deleted: {'Yes' if self.is_deleted else 'No'}"


class Playlist(models.Model):
    emotion = models.CharField(max_length=50, unique=True)
    playlist_url = models.URLField()

    def __str__(self):
        return f"{self.emotion}: {self.playlist_url}"
    

