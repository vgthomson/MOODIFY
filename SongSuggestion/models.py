from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class EmotionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emotion_logs")
    emotion = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.emotion} at {self.timestamp}"
