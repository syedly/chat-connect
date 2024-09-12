from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from task_app.models import Message
from asgiref.sync import sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['user']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_pk']
        self.recipient = await self.get_user(self.recipient_id)

        if self.sender.is_authenticated and self.recipient:
            # Generate a consistent room name by sorting sender and recipient ids
            sorted_ids = sorted([self.sender.id, self.recipient.id])
            self.room_name = f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

            # Join the room
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.save_message(self.sender, self.recipient, message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, sender, recipient, content):
        Message.objects.create(sender=sender, recipient=recipient, content=content)
