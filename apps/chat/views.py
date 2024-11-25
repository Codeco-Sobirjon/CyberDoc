from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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


class CheckReceiverHasView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Chat'],
        operation_summary="Check if a conversation exists",
        operation_description="This endpoint checks whether a conversation exists between the logged-in user "
                              "(initiator) and a specific user (receiver) by their ID.",
        responses={
            302: openapi.Response("Conversation exists (True)"),
            404: openapi.Response("Conversation does not exist (False)"),
        },
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the receiver (CustomUser ID)",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        initiator = request.user
        receiver = get_object_or_404(CustomUser, id=kwargs.get('id'))
        conversation_exists = Conversation.objects.select_related('initiator').filter(
            initiator=initiator
        ).select_related('receiver').filter(
            receiver=receiver
        ).first()
        if conversation_exists:
            serializer = ConversationSerializer(conversation_exists, context={"request": request})
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        return Response({'error': False}, status=status.HTTP_404_NOT_FOUND)

