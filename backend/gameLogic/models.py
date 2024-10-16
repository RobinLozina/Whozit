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
    
class Game(models.Model):
    room_code = models.CharField(max_length=50, unique=True)
    selected_folder = models.CharField(max_length=100)
    creator = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_code

class Player(models.Model):
    room = models.ForeignKey(Room, related_name='players', on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

class Character(models.Model):
    game = models.ForeignKey(Game, related_name='characters', on_delete=models.CASCADE, default=1)  # Set default to Game with ID 1    name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='characters/')

    def __str__(self):
        return self.name