from rest_framework import serializers
from .models import Interest

class InterestSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(read_only=True)
    source = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Interest
        fields = ("keyword", "source", "created_at")
