# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .chat_models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL에서 추출한 chatroom 이름
        self.chatroom = self.scope['url_route']['kwargs']['chatroom']
        self.room_group_name = f'chat_{self.chatroom}'

        # 그룹에 참가 (이 그룹은 WebSocket 메시지를 broadcast 하기 위한 논리적인 공간)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # 클라이언트에서 메시지를 받았을 때 실행됨
        text_data_json = json.loads(text_data)
        input_msg = text_data_json['input_msg']
        user_email = text_data_json['sender']  # Flutter에서 이메일 보내도록 할 예정

        # 사용자 조회 (DB에서 sender 정보 가져오기)
        try:
            sender = await sync_to_async(User.objects.get)(email=user_email)
        except User.DoesNotExist:
            return  # 무시

        # ChatRoom이 없으면 생성
        chatroom_obj, _ = await sync_to_async(ChatRoom.objects.get_or_create)(chatroom=self.chatroom)

        # DB에 메시지 저장
        message_obj = await sync_to_async(Message.objects.create)(
            chatroom=chatroom_obj,
            sender=sender,
            input_msg=input_msg,
            filtered_msg=input_msg,  # 일단 원본 그대로, 나중에 필터링 적용
            created_at=timezone.now()
        )

        # 모든 참가자에게 메시지 전송 (broadcast)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'input_msg': input_msg,
                'sender': user_email,
                'created_at': str(message_obj.created_at),
            }
        )

    async def chat_message(self, event):
        # group_send로부터 받은 메시지를 클라이언트에게 보냄
        await self.send(text_data=json.dumps({
            'input_msg': event['input_msg'],
            'sender': event['sender'],
            'created_at': event['created_at'],
        }))
