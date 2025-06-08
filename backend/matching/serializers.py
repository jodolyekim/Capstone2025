from rest_framework import serializers
from users.models import CustomUser
from .models import Match, ChatRoom, Message


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


class MatchSerializer(serializers.ModelSerializer):
    user1 = UserSummarySerializer(read_only=True)
    user2 = UserSummarySerializer(read_only=True)

    class Meta:
        model = Match
        fields = [
            'id',
            'user1',
            'user2',
            'status_user1',
            'status_user2',
            'matched_keywords',
            'is_matched',
            'matched_at',
            'requested_at',
        ]


class ChatRoomSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    participants = UserSummarySerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'match',
            'participants',
            'created_at',
            'is_active',
            'last_message_at',
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSummarySerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'room',
            'sender',
            'content',
            'sent_at',
            'message_type',
        ]
