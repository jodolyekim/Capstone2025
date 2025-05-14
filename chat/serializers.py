from rest_framework import serializers
from chat.models import Report, Message

class ReportSerializer(serializers.ModelSerializer):
    message = serializers.IntegerField()  # ✅ message를 정수형 ID로 받도록 명시

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
        message = validated_data.pop('message')  # validate_message에서 객체로 변경됨
        return Report.objects.create(reporter=reporter, message=message, **validated_data)
