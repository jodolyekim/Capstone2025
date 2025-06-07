from rest_framework import serializers
from users.models import Match, CustomUser


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
