from rest_framework import serializers
from .models import Room, Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'is_creator', 'joined_at']  # Include fields you want to expose

class RoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)  # Nest the PlayerSerializer

    class Meta:
        model = Room
        fields = ['code', 'created_at', 'game_started', 'players']  # Include players in room data

