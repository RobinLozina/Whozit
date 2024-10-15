from django.db import models
import uuid
from django.urls import reverse

class Room(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    game_started = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('waiting_room', args=[str(self.code)])

class Player(models.Model):
    room = models.ForeignKey(Room, related_name='players', on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)