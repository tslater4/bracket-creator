# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class TournamentBracket(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="brackets")
    created_at = models.DateTimeField(auto_now_add=True)
    size_choices = [
        (4, '4 Participants'),
        (8, '8 Participants'),
        (16, '16 Participants'),
        (32, '32 Participants'),
    ]
    size = models.IntegerField(choices=size_choices, default=8)

class Participant(models.Model):
    name = models.CharField(max_length=100)
    bracket = models.ForeignKey(TournamentBracket, on_delete=models.CASCADE, related_name="participants")

    class Meta:
        ordering = ['id']