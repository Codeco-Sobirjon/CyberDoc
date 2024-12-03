from rest_framework import serializers
from apps.account.serializers import CustomUserDeatilSerializer
from apps.chat.models import Conversation, Message
from apps.chat.utils import custom_user_has_student_role, custom_user_has_author_role


def get_sender_type(self, obj):
    # Get the current user from the request context
    request_user = self.context.get('request').user

    # Check roles of the current user
    student = custom_user_has_student_role(request_user)
    author = custom_user_has_author_role(request_user)

    # Retrieve the conversation and sender from the message
    conversation = obj.conversation_id
    user = obj.sender

    # Determine the initiator and receiver in the conversation
    if student and conversation.student == user:
        return 'initiator' if conversation.created_by == user else 'receiver'

    if author and conversation.author == user:
        return 'initiator' if conversation.created_by == user else 'receiver'

    # If no match, return None or a default value
    return None


class MessageListSerializer(serializers.ModelSerializer):
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
            return MessageSerializer(instance=message, context={'request': self.context.get('request')}).data
        return None


class ConversationSerializer(serializers.ModelSerializer):
    initiator = CustomUserDeatilSerializer()
    receiver = CustomUserDeatilSerializer()
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'message_set']
