import json
import django
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guessWho.settings')
django.setup()

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
                        
                        # Broadcast the game started event along with the characters to the room group
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
                        await self.channel_layer.group_send(
                            f'game_room_{self.room_code}',
                            {
                                'type': 'game_start',
                                'message': {
                                    'event': 'game_started',
                                    'characters': game_data['characters'],
                                    'room_code': game_data['room_code'],
                                }
                            }
                        )

                elif event == 'chat':
                    # Broadcast the message to the room group
                    message = text_data_json.get('message', '')
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                'event': 'chat',
                                'message': message
                            }
                        }
                    )

            else:
                # Handle case where the data does not match any known structure
                print("Error: Unrecognized data format.")
        
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

        print(f"Attempting connection for game room code: {self.room_code}")

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
            text_data_json = json.loads(text_data)

            if 'event' in text_data_json:
                event = text_data_json['event']

                if event == 'chat':
                    # Broadcast the message to the room group
                    message = text_data_json.get('message', '')
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                'event': 'chat',
                                'message': message
                            }
                        }
                    )

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    # Receive message from the room group
    async def game_start(self, event):
        # Handle the game start event with characters
        message = event['message']

        # Send the message to the WebSocket (including characters)
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