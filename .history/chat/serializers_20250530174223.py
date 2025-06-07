from rest_framework import serializers
from .models import ChatRoom, Message, Report
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


# ✅ 신고 요청 직렬화
class ReportSerializer(serializers.ModelSerializer):
    message = serializers.IntegerField()  # ID로 받음

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
        message = validated_data.pop('message')  # validate_message에서 교체됨
        return Report.objects.create(reporter=reporter, message=message, **validated_data)
