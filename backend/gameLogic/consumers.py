import json
from channels.generic.websocket import AsyncWebsocketConsumer

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
                    # Handle the start game event
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {'event': 'game_started'}
                        }
                    )

            elif 'message' in text_data_json:
                message = text_data_json['message']

                # Broadcast the message to the room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
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
    async def chat_message(self, event):
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
            # Print the received data for debugging
            print(f"Received data: {text_data}")

            # Parse the incoming data
            text_data_json = json.loads(text_data)

            # Handle different event types
            if 'event' in text_data_json:
                event = text_data_json['event']

                if event == 'start_game':
                    # Handle the start game event
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {'event': 'game_started'}
                        }
                    )

            elif 'message' in text_data_json:
                message = text_data_json['message']

                # Broadcast the message to the room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
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
    async def chat_message(self, event):
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
