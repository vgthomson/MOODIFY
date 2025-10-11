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


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Playlist(models.Model):
    emotion = models.CharField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    playlist_url = models.URLField()

    class Meta:
        unique_together = ('emotion', 'language')  # Ensures no duplicate playlist for same emotion and language.

    def __str__(self):
        return f"{self.emotion} ({self.language}): {self.playlist_url}"
    

class Feedback(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    title = models.CharField(max_length=200)
    suggestion = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_note = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.title}"
    

