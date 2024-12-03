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
        # Get the logged-in user from the request context
        request_user = self.context.get('request').user

        # Determine the role of the logged-in user
        is_student = custom_user_has_student_role(request_user)
        is_author = custom_user_has_author_role(request_user)

        # Fetch conversation and sender details
        conversation = obj.conversation_id
        sender = obj.sender

        # Logic for students
        if is_student and request_user == conversation.initiator:
            # If the logged-in user is a student and the initiator
            return 'initiator' if sender == request_user else 'receiver'

        # Logic for authors
        if is_author and request_user == conversation.receiver:
            # If the logged-in user is an author and the receiver
            return 'receiver' if sender == request_user else 'initiator'

        # Default case
        return 'unknown'


        # if user:
        #     if student or author:
        #         if conversation.initiator == user:
        #             return 'initiator'
        #         elif conversation.receiver == user:
        #             return 'receiver'
        #     return 'unknown'


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
