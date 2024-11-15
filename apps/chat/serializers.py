from rest_framework import serializers
from apps.account.models import CustomUser
from apps.account.serializers import CustomUserDeatilSerializer
from apps.chat.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserDeatilSerializer()
    class Meta:
        model = Message
        exclude = ('conversation_id',)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = CustomUserDeatilSerializer()
    receiver = CustomUserDeatilSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        if message:
            return MessageSerializer(instance=message).data
        return None


class ConversationSerializer(serializers.ModelSerializer):
    initiator = CustomUserDeatilSerializer()
    receiver = CustomUserDeatilSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'message_set']
