from django.db import models
from apps.users.models import User


class ConnectionStatus(models.TextChoices):
    pending =("pending", "Pending")
    accepted = ("accepted","Accepted")
    rejected = ("rejected", "Rejected")



class ConnectionRequests(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=ConnectionStatus.choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Request sent by {self.sender.full_name} to {self.receiver.full_name} and status is {self.status}"
    