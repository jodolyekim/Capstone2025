from rest_framework import serializers
from .models import ChatRoom, Message, Report, ChatReport
from users.models import CustomUser


# ✅ CustomUser 최소 정보 직렬화
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


# ✅ 메시지 직렬화
class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'chatroom',
            'sender',
            'input_msg',
            'filtered_msg',
            'msg_type',
            'created_at',
            'format_filtered',
            'gpt_filtered',
            'reason',
        ]


# ✅ 채팅방 직렬화 (참여자 + 메시지)
class ChatRoomSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'chatroom',
            'participants',
            'messages',
            'created_at',
        ]


# ✅ 메시지 단위 신고 직렬화기
class ReportSerializer(serializers.ModelSerializer):
    message = serializers.IntegerField()  # 메시지 ID로 받음

    class Meta:
        model = Report
        fields = ['message', 'reason']

    def validate_message(self, value):
        try:
            return Message.objects.get(id=value)
        except Message.DoesNotExist:
            raise serializers.ValidationError("해당 메시지를 찾을 수 없습니다.")

    def create(self, validated_data):
        reporter = self.context['request'].user
        message = validated_data.pop('message')
        return Report.objects.create(reporter=reporter, message=message, **validated_data)


# ✅ 채팅방 단위 신고 직렬화기
class ChatReportSerializer(serializers.ModelSerializer):
    chat_room = serializers.UUIDField()  # 문자열 UUID 가능
    reported = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = ChatReport
        fields = [
            'chat_room',
            'reported',
            'reason',
            'custom_reason',
            'message_snapshot',
        ]

    def validate_chat_room(self, value):
        try:
            return ChatRoom.objects.get(id=value)
        except ChatRoom.DoesNotExist:
            raise serializers.ValidationError("해당 채팅방을 찾을 수 없습니다.")

    def create(self, validated_data):
        reporter = self.context['request'].user
        chat_room = validated_data.pop('chat_room')  # validate_chat_room에서 대체됨
        return ChatReport.objects.create(reporter=reporter, chat_room=chat_room, **validated_data)

