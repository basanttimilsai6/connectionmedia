from rest_framework import serializers
from apps.connections.models import ConnectionRequests
from apps.users.models import User


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']


class ConnectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequests
        fields = ['receiver']

    def validate_receiver(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("You cannot send a request to yourself.")
        return value

    def create(self, validated_data):
        return ConnectionRequests.objects.create(
            sender=self.context['request'].user,
            **validated_data
        )


class ConnectionRequestSerializer(serializers.ModelSerializer):
    sender = UserBriefSerializer(read_only=True)
    receiver = UserBriefSerializer(read_only=True)

    class Meta:
        model = ConnectionRequests
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']
        read_only_fields = ['sender', 'receiver', 'created_at']


class ConnectionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequests
        fields = ['status']

    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Only 'accepted' or 'rejected' status is allowed.")
        return value