from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender_messages', on_delete=models.CASCADE)
    recipient  = models.ForeignKey(User, related_name='recipient_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.recipient.username}'