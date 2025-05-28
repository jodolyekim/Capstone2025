import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message
from .utils.message_filtering import check_predefined_patterns
from .utils.gpt_judge import is_sensitive_message

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
            # 1. 메시지 파싱
            data = json.loads(text_data)
            input_msg = data.get('input_msg', '')
            user_email = data.get('sender', '')
            msg_type = data.get('type', 'text')
            print("✅ 파싱 성공:", input_msg, user_email, msg_type)

            # 필터 관련 상태 초기화
            detected = []
            reason = ""
            format_filtered = False
            gpt_filtered = False

            # 2. 이미지 메시지는 필터링 건너뜀
            if msg_type != 'image':
                detected = check_predefined_patterns(input_msg)

                # join 안전 처리
                if isinstance(detected, list):
                    format_filtered = len(detected) > 0
                    reason = '/'.join(detected)
                elif isinstance(detected, str):
                    format_filtered = True
                    reason = detected
                    detected = [detected]
                else:
                    format_filtered = False
                    reason = ""

                if format_filtered:
                    print("⛔ 형식 필터 감지됨:", reason)

                    # 3. GPT 판단 시도
                    try:
                        print("📤 GPT 판단 요청:", input_msg)
                        gpt_filtered = await sync_to_async(is_sensitive_message)(input_msg)
                        print("🧠 GPT 판단 결과:", gpt_filtered)
                    except Exception as gpt_error:
                        print("❌ GPT 호출 실패:", str(gpt_error))
                        await self.send(text_data=json.dumps({
                            'input_msg': "🚫 일시적으로 메시지를 보낼 수 없습니다. 잠시 후 다시 시도해주세요.",
                            'sender': 'SYSTEM',
                            'type': 'text',
                            'created_at': str(timezone.now())
                        }))
                        return

                    if gpt_filtered:
                        warning_msg = f"🚫 전송이 차단되었습니다: {reason} 포함됨"
                        await self.send(text_data=json.dumps({
                            'input_msg': warning_msg,
                            'sender': 'SYSTEM',
                            'type': 'text',
                            'created_at': str(timezone.now())
                        }))
                        print("⛔ 최종 차단됨 (GPT 판단 포함):", reason)

                        # 차단된 메시지 저장
                        sender = await sync_to_async(User.objects.get)(email=user_email)
                        chatroom_obj, _ = await sync_to_async(ChatRoom.objects.get_or_create)(chatroom=self.chatroom)
                        await sync_to_async(Message.objects.create)(
                            chatroom=chatroom_obj,
                            sender=sender,
                            input_msg=input_msg,
                            filtered_msg=input_msg,
                            msg_type=msg_type,
                            created_at=timezone.now(),
                            format_filtered=True,
                            gpt_filtered=True,
                            reason=reason
                        )
                        return
                    else:
                        print("✅ GPT 판단 통과 → 메시지 전송 허용")
                else:
                    print("✅ 형식 필터 통과")

            else:
                print("✅ 이미지 메시지 필터링 건너뜀")

            # 4. 사용자 및 채팅방 조회
            sender = await sync_to_async(User.objects.get)(email=user_email)
            print("✅ 유저 조회 성공:", sender)
            chatroom_obj, _ = await sync_to_async(ChatRoom.objects.get_or_create)(chatroom=self.chatroom)
            print("✅ 채팅방 준비 완료")

            # 5. 메시지 저장
            saved_msg = await sync_to_async(Message.objects.create)(
                chatroom=chatroom_obj,
                sender=sender,
                input_msg=input_msg,
                filtered_msg=input_msg,
                msg_type=msg_type,
                created_at=timezone.now(),
                format_filtered=format_filtered,
                gpt_filtered=gpt_filtered,
                reason=reason
            )
            print("✅ 메시지 저장 성공")

            # 6. 메시지 그룹 브로드캐스트
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'input_msg': input_msg,
                    'sender': user_email,
                    'msg_type': msg_type,
                    'created_at': str(saved_msg.created_at),
                }
            )

        except Exception as e:
            print("⛔ 예외 발생:", str(e))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'input_msg': event['input_msg'],
            'sender': event['sender'],
            'type': event.get('msg_type', 'text'),
            'created_at': event['created_at'],
        }))
