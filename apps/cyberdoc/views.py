from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from apps.cyberdoc.filters import OrderWorkFilter
from apps.cyberdoc.models import TypeConsultation, QualificationAuthor, Shrift, Guarantee, OrderWork, DescribeProblem, \
    Portfolio
from apps.cyberdoc.pagination import OrderWorkPagination
from apps.cyberdoc.serializers import TypeConsultationSerializer, QualificationAuthorSerializer, ShriftSerializer, \
    GuaranteeSerializer, OrderWorkSerializer, OrderWorkCreateAndUpdateSerializer, OrderWorkReviewSerializer, \
    DescribeProblemSerializer, DescribeProblemListSerializer, PortfolioSerializer, PortfolioListSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TypeConsultationListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["CyberDoc"],
        operation_description="Retrieve a list of all TypeConsultations",
        responses={200: TypeConsultationSerializer(many=True)},
    )
    def get(self, request):
        consultations = TypeConsultation.objects.all()
        serializer = TypeConsultationSerializer(consultations, many=True)
        return Response(serializer.data)


class QualificationAuthorListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["CyberDoc"],
        operation_description="Retrieve a list of all QualificationAuthors",
        responses={200: QualificationAuthorSerializer(many=True)},
    )
    def get(self, request):
        authors = QualificationAuthor.objects.all()
        serializer = QualificationAuthorSerializer(authors, many=True)
        return Response(serializer.data)


class ShriftListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["CyberDoc"],
        operation_description="Retrieve a list of all Shrifts",
        responses={200: ShriftSerializer(many=True)},
    )
    def get(self, request):
        shrifts = Shrift.objects.all()
        serializer = ShriftSerializer(shrifts, many=True)
        return Response(serializer.data)


class GuaranteeListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["CyberDoc"],
        operation_description="Retrieve a list of all Guarantees",
        responses={200: GuaranteeSerializer(many=True)},
    )
    def get(self, request):
        guarantees = Guarantee.objects.all()
        serializer = GuaranteeSerializer(guarantees, many=True)
        return Response(serializer.data)


class OrderWorkListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = OrderWorkPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = OrderWorkFilter

    @swagger_auto_schema(
        tags=["CyberDoc order works"],
        operation_description="Retrieve a list of all OrderWorks with filtering and pagination",
        responses={200: OrderWorkSerializer(many=True)},
        parameters=[
            openapi.Parameter('number_of_order', openapi.IN_QUERY, description="Filter by number of order",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('deadline', openapi.IN_QUERY, description="Filter by deadline (less than or equal to)",
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number for pagination",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page",
                              type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request):

        orders = OrderWork.objects.select_related('author').filter(author=request.user)

        filtered_orders = OrderWorkFilter(request.GET, queryset=orders).qs

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_orders, request)

        serializer = OrderWorkSerializer(page, many=True, context={'request': request})

        return paginator.get_paginated_response(serializer.data)


class OrderWorkDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["CyberDoc order works"],
        operation_description="Retrieve details of a specific OrderWork",
        responses={200: OrderWorkSerializer},
    )
    def get(self, request, pk):
        order = get_object_or_404(OrderWork, pk=pk)
        
        serializer = OrderWorkSerializer(order, context={'request': request})
        return Response(serializer.data)


class OrderWorkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["CyberDoc order works"],
        operation_description="Create a new OrderWork",
        request_body=OrderWorkCreateAndUpdateSerializer,
        responses={201: OrderWorkCreateAndUpdateSerializer},
    )
    def post(self, request):
        serializer = OrderWorkCreateAndUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Successfully created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderWorkUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["CyberDoc order works"],
        operation_description="Update an existing OrderWork",
        request_body=OrderWorkCreateAndUpdateSerializer,
        responses={200: OrderWorkCreateAndUpdateSerializer},
    )
    def put(self, request, pk):
        order = get_object_or_404(OrderWork, pk=pk)

        serializer = OrderWorkCreateAndUpdateSerializer(order, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Successfully updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderWorkDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["CyberDoc order works"],
        operation_description="Delete a specific OrderWork",
        responses={204: 'No Content'},
    )
    def delete(self, request, pk):
        order = get_object_or_404(OrderWork, pk=pk)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderWorkReviewListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Review order work'],
        request_body=OrderWorkReviewSerializer,
        responses={
            201: OrderWorkReviewSerializer,
            400: "Bad request",
            401: "Unauthorized"
        },
        operation_description="Create a new review for an order."
    )
    def post(self, request, *args, **kwargs):
        serializer = OrderWorkReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DescribeProblemListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Describe Problem"],
        operation_description="Retrieve a list of all DescribeProblem instances.",
        responses={200: DescribeProblemListSerializer(many=True)},
    )
    def get(self, request):
        queryset = DescribeProblem.objects.select_related('user').filter(
            user=request.user
        )
        serializer = DescribeProblemListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Describe Problem"],
        operation_description="Create a new DescribeProblem instance.",
        request_body=DescribeProblemSerializer,
        responses={201: DescribeProblemSerializer},
    )
    def post(self, request):
        serializer = DescribeProblemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"msg": "Successfully added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Portfolio'],
        operation_description="Retrieve all portfolio entries",
        responses={200: PortfolioListSerializer(many=True)},
    )
    def get(self, request):
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioListSerializer(portfolios, many=True, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Portfolio'],
        operation_description="Create a new portfolio entry",
        request_body=PortfolioSerializer,
        responses={201: PortfolioSerializer},
    )
    def post(self, request):
        serializer = PortfolioSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


permission_classes = [IsAuthenticated]


class PortfolioDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Portfolio'],
        operation_description="Retrieve a portfolio entry by ID",
        responses={200: PortfolioListSerializer},
    )
    def get(self, request, pk):
        portfolio = get_object_or_404(Portfolio, pk=pk)
        portfolio.views += 1
        portfolio.save()
        serializer = PortfolioListSerializer(portfolio, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Portfolio'],
        operation_description="Update a portfolio entry by ID",
        request_body=PortfolioSerializer,
        responses={200: PortfolioSerializer},
    )
    def put(self, request, pk):
        portfolio = get_object_or_404(Portfolio, pk=pk)
        serializer = PortfolioSerializer(portfolio, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Portfolio'],
        operation_description="Delete a portfolio entry by ID",
        responses={204: 'No Content'},
    )
    def delete(self, request, pk):
        portfolio = get_object_or_404(Portfolio, pk=pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
