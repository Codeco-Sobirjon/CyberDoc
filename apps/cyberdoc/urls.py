from django.urls import path
from apps.cyberdoc.views import *


urlpatterns = [
    path('type-consultation/', TypeConsultationListAPIView.as_view(), name='type_consultation_list'),
    path('qualification-author/', QualificationAuthorListAPIView.as_view(), name='qualification_author_list'),
    path('shrift/', ShriftListAPIView.as_view(), name='shrift_list'),
    path('guarantee/', GuaranteeListAPIView.as_view(), name='guarantee_list'),

    path('orderworks/', OrderWorkListAPIView.as_view(), name='orderwork-list'),
    path('orderworks/<int:pk>/', OrderWorkDetailAPIView.as_view(), name='orderwork-detail'),
    path('orderworks/create/', OrderWorkCreateAPIView.as_view(), name='orderwork-create'),
    path('orderworks/<int:pk>/update/', OrderWorkUpdateAPIView.as_view(), name='orderwork-update'),
    path('orderworks/<int:pk>/delete/', OrderWorkDeleteAPIView.as_view(), name='orderwork-delete'),

    path('reviews/', OrderWorkReviewListCreateAPIView.as_view(), name='orderworkreview-list-create'),

    path('problems/', DescribeProblemListCreateAPIView.as_view(), name='describe_problem_list_create'),

    path('portfolio/', PortfolioListView.as_view(), name='portfolio_list_create'),
    path('porfolio/<int:id>/', PortfolioDetailView.as_view(), name='portfolio_list_create'),
]