import json
import django
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import asyncio
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guessWho.settings')
django.setup()

connected_players = {}  # Track the players in each game room
games_data = {}  # Store game data for each room code

# Now import Django settings or models
from gameLogic.game_logic import initialize_game
class WaitingRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the room code from the URL parameters (scope)
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'waiting_room_{self.room_code}'

        print(f"Attempting connection for room code: {self.room_code}")

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            # Print the received data for debugging
            print(f"Received data: {text_data}")

            # Parse the incoming data
            text_data_json = json.loads(text_data)

            # Handle different event types
            if 'event' in text_data_json:
                event = text_data_json['event']

                if event == 'start_game':
                    # Handle the start game event with selected folder
                    selected_folder = text_data_json.get('folder')
                    if selected_folder:
                        # Use sync_to_async to run the initialize_game function in a thread-safe way
                        game_data = await sync_to_async(initialize_game)(self.room_code, selected_folder)
                        games_data[self.room_code] = game_data

                        # Broadcast the game started event along with the characters to the room group
                        print(f"Broadcasting game start event to room group: {self.room_group_name}")

                        # First, send the game start event to all players in the waiting room
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'game_start',
                                'message': {
                                    'event': 'game_started',
                                    'characters': game_data['characters'],
                                    'room_code': game_data['room_code'],
                                }
                            }
                        )

        except json.JSONDecodeError as e:
            # Handle JSON parsing error
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            # Handle any other exceptions
            print(f"Unexpected error: {e}")

    # Receive message from the room group
    async def game_start(self, event):
        # Handle the game start event
        message = event['message']

        # Send the message to the WebSocket with the list of characters
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def chat_message(self, event):
        # Handle a chat message
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'game_room_{self.room_code}'

        print(f"GameRoomConsumer attempting connection for game room code: {self.room_code}")

        # Join the game room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f"GameRoomConsumer joined group: {self.room_group_name}")

        await self.accept()
        print("GameRoomConsumer WebSocket connection accepted.")

        # Add player to the connected players tracker
        if self.room_code not in connected_players:
            connected_players[self.room_code] = 0
        connected_players[self.room_code] += 1

        print(f"Number of players connected in room {self.room_code}: {connected_players[self.room_code]}")

        # If both players are connected, trigger game start
        if connected_players[self.room_code] >= 2:
            await self.start_game()

    async def disconnect(self, close_code):
        # Leave the game room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"GameRoomConsumer left group: {self.room_group_name}")

        if self.room_code in connected_players:
            connected_players[self.room_code] -= 1
            if connected_players[self.room_code] <= 0:
                del connected_players[self.room_code]  # Remove the room if no players left

    async def start_game(self):
        if self.room_code in games_data:
            game_data = games_data[self.room_code]

            # Broadcast game start event with character data
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_start',
                    'message': {
                        'event': 'game_started',
                        'characters': game_data['characters'],
                        'room_code': self.room_code,
                    }
                }
            )
            print(f"Game started for room: {self.room_code}")

    async def game_start(self, event):
        message = event['message']
        print(f"GameRoomConsumer received game start event: {message}")

        # Send the message to the WebSocket (including characters)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)

            if 'event' in text_data_json:
                event = text_data_json['event']

                if event == 'chat':
                    message = text_data_json.get('message', '')
                    # Broadcast the chat message to the game room group
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                'event': 'chat',
                                'message': message,
                            }
                        }
                    )

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    async def chat_message(self, event):
        message = event['message']
        print(f"GameRoomConsumer received chat message: {message}")

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))