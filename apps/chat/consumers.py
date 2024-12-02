import base64
import json
import secrets
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from apps.account.models import CustomUser
from apps.chat.models import Message, Conversation
from apps.chat.serializers import MessageSerializer, MessageListSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        # Log when group_send is called
        print(f"Sending to group: {self.room_group_name}, data: {return_dict}")
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )

        # Check if the conversation exists
        try:
            conversation = Conversation.objects.get(id=int(self.room_name))
        except Conversation.DoesNotExist:
            print(f"Conversation {self.room_name} does not exist.")
            return

        sender = self.scope['user']

        # Check if the message is already created (optional safeguard)
        if Message.objects.filter(
                sender=sender, text=message, conversation_id=conversation
        ).exists():
            print("Duplicate message detected, skipping creation.")
            return

        # Create the message
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]
            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = Message.objects.create(
                sender=sender,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
            )
        else:
            _message = Message.objects.create(
                sender=sender,
                text=message,
                conversation_id=conversation,
            )

        # Serialize and send back the message
        serializer = MessageListSerializer(instance=_message)

        self.send(
            text_data=json.dumps(
                serializer.data
            )
        )
