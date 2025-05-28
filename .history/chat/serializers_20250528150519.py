from rest_framework import serializers
from .models import ChatRoom, Message
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


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
