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

        # Debug log
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
            sender_id = event["sender_id"]
            message = event.get("message", "")
            attachment = event.get("attachment")

            # Debug log
            print(f"Received message for room: {self.room_group_name}, from sender: {sender_id}")

            # Fetch sender
            sender = CustomUser.objects.filter(id=sender_id).first()
            if not sender:
                print(f"Sender with ID {sender_id} not found.")
                self.send(text_data=json.dumps({"error": "Sender not found"}))
                return

            # Fetch conversation
            try:
                conversation_id = int(self.room_name)  # Assuming `room_name` is the conversation ID
                conversation = Conversation.objects.get(id=conversation_id)
            except (ValueError, Conversation.DoesNotExist):
                print(f"Invalid conversation ID: {self.room_name}")
                self.send(text_data=json.dumps({"error": "Conversation not found"}))
                return

            # Create message
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
                        conversation=conversation,
                    )
                except Exception as e:
                    print(f"Attachment handling failed: {e}")
                    self.send(text_data=json.dumps({"error": "Invalid attachment"}))
                    return
            else:
                new_message = Message.objects.create(
                    sender=sender, text=message, conversation=conversation
                )

            # Serialize and send the created message
            serializer = MessageListSerializer(instance=new_message)
            print(f"Message saved successfully: {serializer.data}")
            self.send(text_data=json.dumps(serializer.data))

        except Exception as e:
            print(f"Error processing chat message: {e}")
            self.send(text_data=json.dumps({"error": "Failed to process message"}))
