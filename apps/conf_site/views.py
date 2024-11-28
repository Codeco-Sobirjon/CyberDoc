from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.conf_site.models import Service, SubmitRequest, ServiceBlog
from apps.conf_site.serializers import ServiceSerializer, SubmitRequestSerializer, ServiceBlogSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ServiceListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all services with their details.",
        tags=['Configuration site'],
        responses={200: ServiceSerializer(many=True)}
    )
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitRequestCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new submit request.",
        tags=['Configuration site'],
        request_body=SubmitRequestSerializer,
        responses={201: SubmitRequestSerializer},
    )
    def post(self, request):
        serializer = SubmitRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceBlogListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get list of all service blogs",
        tags=['Configuration site'],
        responses={200: ServiceBlogSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        blogs = ServiceBlog.objects.all()
        serializer = ServiceBlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)