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

        # Add the channel to the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Remove the channel from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")
            attachment = text_data_json.get("attachment")

            sender = self.scope["user"]
            if sender.is_anonymous:
                self.send(
                    text_data=json.dumps({"error": "Authentication failed"})
                )
                return

            # Debug log
            print(f"Broadcasting message from sender: {sender.id}")

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "attachment": attachment,
                    "sender_id": sender.id,
                },
            )
        except Exception as e:
            self.send(text_data=json.dumps({"error": str(e)}))

    def chat_message(self, event):
        try:
            message = event["message"]
            attachment = event.get("attachment")
            sender_id = event["sender_id"]

            # Prevent duplicate sending
            print(f"Processing message from sender: {sender_id}, message: {message}")

            sender = CustomUser.objects.get(id=sender_id)
            conversation = Conversation.objects.get(id=int(self.room_name))

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
                    sender=sender, text=message, conversation_id=conversation
                )

            serializer = MessageListSerializer(instance=_message)
            self.send(text_data=json.dumps(serializer.data))
        except Exception as e:
            self.send(text_data=json.dumps({"error": str(e)}))
