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

import traceback


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        print(f"Adding channel: {self.channel_name} to group: {self.room_group_name}")

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print(f"Removing channel: {self.channel_name} from group: {self.room_group_name}")
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
                self.send(text_data=json.dumps({"error": "Authentication failed"}))
                return

            print(f"Received message: {message} from {sender.id}")

            try:
                conversation_id = int(self.room_name)
                conversation = Conversation.objects.get(id=conversation_id)
            except (ValueError, Conversation.DoesNotExist) as e:
                raise ValueError(f"Invalid conversation ID: {self.room_name}") from e

            if attachment:
                try:
                    file_str = attachment["data"]
                    file_ext = attachment["format"]
                    file_data = ContentFile(
                        base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
                    )
                    new_message = Message.objects.create(
                        sender=sender,
                        attachment=file_data,
                        text=message,
                        conversation_id=conversation,
                    )
                except Exception as e:
                    raise ValueError(f"Attachment processing failed: {e}") from e
            else:
                new_message = Message.objects.create(
                    sender=sender, text=message, conversation_id=conversation
                )

            print(f"Message successfully saved: {new_message.id}")

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message_id": new_message.id,
                },
            )
        except Exception as e:
            self.send(text_data=json.dumps({"error": str(e)}))

    def chat_message(self, event):
        try:
            print(f"Received event: {event}")

            message_id = event.get("message_id")

            new_message = Message.objects.filter(id=message_id).first()
            if not new_message:
                raise ValueError(f"Message with ID {message_id} not found.")

            serialized_message = MessageListSerializer(new_message, context={'request': self.scope["user"]}).data

            self.send(text_data=json.dumps(serialized_message))

        except Exception as e:

            print(f"Error processing chat message: {e}")
            traceback.print_exc()
            self.send(text_data=json.dumps({"error": f"Failed to process message: {str(e)}"}))




