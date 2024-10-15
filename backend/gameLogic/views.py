from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from .models import Room, Player
from .serializers import RoomSerializer, PlayerSerializer
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the Guess Who API. The frontend is served separately.")

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        room = Room.objects.create()
        player = Player.objects.create(room=room, is_creator=True)  # First player is the creator
        serializer = self.get_serializer(room)
        return Response(serializer.data)

class JoinRoomView(APIView):
    def post(self, request, code, format=None):
        try:
            room = Room.objects.get(code=code)
            if room.players.count() >= 2:
                return Response({"error": "Room is full."}, status=status.HTTP_403_FORBIDDEN)
            if room.game_started:
                return Response({"error": "Game has already started."}, status=status.HTTP_403_FORBIDDEN)

            # Create the player and add to room
            player = Player.objects.create(room=room, is_creator=False)

            # Serialize players in the room
            players_data = PlayerSerializer(room.players.all(), many=True).data

            # Send a message to all players via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'waiting_room_{room.code}',
                {
                    'type': 'chat_message',
                    'message': {
                        'event': 'player_joined',
                        'players': players_data
                    }
                }
            )

            return Response({
                "message": "Joined room successfully.",
                "player_id": player.id,
                "is_creator": player.is_creator,
                "room_code": str(room.code),
                "players": players_data,
            }, status=status.HTTP_201_CREATED)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        
class WaitingRoomView(APIView):
    def get(self, request, code, format=None):
        try:
            room = Room.objects.get(code=code)
            serializer = RoomSerializer(room)
            # Add logic here to identify the current player
            player_id = request.query_params.get('player_id')  # Player ID from frontend
            is_creator = room.players.filter(id=player_id, is_creator=True).exists()
            return Response({
                "room": serializer.data,
                "is_creator": is_creator
            }, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)


class StartGameView(APIView):
    def post(self, request, code, format=None):
        try:
            room = Room.objects.get(code=code)
            if room.game_started:
                return Response({"error": "Game already started."}, status=status.HTTP_400_BAD_REQUEST)
            
            room.game_started = True
            room.save()

            # Send a message to all players via WebSocket to indicate game start
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'waiting_room_{room.code}',
                {
                    'type': 'chat_message',
                    'message': {
                        'event': 'game_started',
                        'room_code': room.code
                    }
                }
            )

            return Response({"message": "Game started successfully."}, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)