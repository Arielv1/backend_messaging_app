from rest_framework import serializers
from .models import Message
import uuid
from django.utils import timezone


class MessageSerializer(serializers.ModelSerializer):
    was_read = serializers.BooleanField(default=False)

    class Meta:
        model = Message
        fields = ('message_id', 'sender', 'receiver',
                  'subject', 'message', 'was_read')
        extra_kwargs = {
            'was_read': {'write_only': True},
        }
