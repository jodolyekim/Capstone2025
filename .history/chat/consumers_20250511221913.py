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
        print(f"✅ WebSocket 연결됨: {self.chatroom}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"🔌 WebSocket 연결 종료: {self.chatroom}")

    async def receive(self, text_data):
        print("🟡 받은 메시지:", text_data)

        try:
            print("1️⃣ JSON 파싱 시작")
            text_data_json = json.loads(text_data)
            input_msg = text_data_json.get('input_msg', '')
            user_email = text_data_json.get('sender', '')
            print("✅ 파싱 성공:", input_msg, user_email)

            print("2️⃣ 유저 조회 시도")
            sender = await sync_to_async(User.objects.get)(email=user_email)
            print("✅ 유저 조회 성공:", sender)

            print("3️⃣ 채팅방 조회 또는 생성 시도")
            chatroom_obj, _ = await sync_to_async(ChatRoom.objects.get_or_create)(chatroom=self.chatroom)
            print("✅ 채팅방 조회 또는 생성 성공:", chatroom_obj)

            print("4️⃣ 메시지 저장 시도")
            saved_msg = await sync_to_async(Message.objects.create)(
                chatroom=chatroom_obj,
                sender=sender,
                input_msg=input_msg,
                filtered_msg=input_msg,
                created_at=timezone.now()
            )
            print("✅ DB 저장 성공:", saved_msg)

            print("5️⃣ 그룹에 메시지 브로드캐스트 시도")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'input_msg': input_msg,
                    'sender': user_email,
                    'created_at': str(saved_msg.created_at),
                }
            )

        except Exception as e:
            print("⛔ 예외 발생:", str(e))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'input_msg': event['input_msg'],
            'sender': event['sender'],
            'created_at': event['created_at'],
        }))
