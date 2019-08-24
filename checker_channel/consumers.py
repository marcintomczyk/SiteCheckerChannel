# checker_channel/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CheckerChannelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'checker_channel_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        url = text_data_json['url']
        message = text_data_json['message']
        timestamp = text_data_json['timestamp']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'channel_message',
                'url': url,
                'message': message,
                'timestamp': timestamp
            }
        )

    # Receive message from room group
    async def channel_message(self, event):
        message = event['message']
        url = event['url']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'url': url,
            'timestamp': timestamp
        }))