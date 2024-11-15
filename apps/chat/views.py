from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, reverse, get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.account.models import CustomUser
from apps.chat.models import Conversation
from apps.chat.serializers import ConversationSerializer, ConversationListSerializer


class StartConversationView(APIView):
    @swagger_auto_schema(
        tags=['Chat'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description="Phone number of the participant"),
            }
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Conversation started",
                schema=ConversationSerializer,
            ),
            status.HTTP_302_FOUND: openapi.Response(
                description="Redirect to existing conversation",
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data.pop('phone')
        participant = get_object_or_404(CustomUser, phone=phone)

        conversation = Conversation.objects.filter(
            Q(initiator=request.user, receiver=participant) |
            Q(initiator=participant, receiver=request.user)
        )

        if conversation.exists():
            return redirect(reverse('get_conversation', args=(conversation[0].id,)))
        else:
            conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
            return Response(ConversationSerializer(instance=conversation).data, status=status.HTTP_201_CREATED)


class GetConversationView(APIView):
    @swagger_auto_schema(
        tags=['Chat'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Conversation details",
                schema=ConversationSerializer,
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        conversation = get_object_or_404(Conversation, id=kwargs.get('convo_id'))
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConversationListView(APIView):
    @swagger_auto_schema(
        tags=['Chat'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of conversations",
                schema=ConversationListSerializer(many=True),
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        conversation_list = Conversation.objects.filter(
            Q(initiator=request.user) |
            Q(receiver=request.user)
        )
        serializer = ConversationListSerializer(conversation_list, many=True)
        return Response(serializer.data)


