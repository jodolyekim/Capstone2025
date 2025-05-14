# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom = self.scope['url_route']['kwargs']['chatroom']
        self.room_group_name = f'chat_{self.chatroom}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print("🟡 받은 메시지:", text_data)

        try:
            text_data_json = json.loads(text_data)
            input_msg = text_data_json['input_msg']
            user_email = text_data_json['sender']

            sender = await sync_to_async(User.objects.get)(email=user_email)
            chatroom_obj, _ = await sync_to_async(ChatRoom.objects.get_or_create)(chatroom=self.chatroom)

            await sync_to_async(Message.objects.create)(
                chatroom=chatroom_obj,
                sender=sender,
                input_msg=input_msg,
                filtered_msg=input_msg,
                created_at=timezone.now()
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'input_msg': input_msg,
                    'sender': user_email,
                    'created_at': str(timezone.now()),
                }
            )

        except Exception as e:
            print("⛔ 저장 실패:", str(e))  # DB 저장 실패 로그

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'input_msg': event['input_msg'],
            'sender': event['sender'],
            'created_at': event['created_at'],
        }))
