from rest_framework import serializers
from apps.account.serializers import CustomUserDeatilSerializer
from apps.chat.models import Conversation, Message
from apps.chat.utils import custom_user_has_student_role, custom_user_has_author_role


class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserDeatilSerializer()
    sender_type = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'sender_type', 'timestamp']

    def get_sender_type(self, obj):

        student = custom_user_has_student_role(self.context.get('request').user)
        author = custom_user_has_author_role(self.context.get('request').user)

        conversation = obj.conversation_id
        user = obj.sender

        if user:
            if student or author:
                if conversation.initiator == user:
                    return 'initiator'
                elif conversation.receiver == user:
                    return 'receiver'
            # if :
            #     if conversation.initiator == user:
            #         return 'receiver'
            #     elif conversation.receiver == user:
            #         return 'initiator'
            return 'unknown'


class MessageListSerializer(serializers.ModelSerializer):
    sender = CustomUserDeatilSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp']


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
