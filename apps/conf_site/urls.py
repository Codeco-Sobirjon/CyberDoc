from django.urls import path
from apps.conf_site.views import *

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('service-blogs/', ServiceBlogListAPIView.as_view(), name='service_blog_list'),
    path('submit_requests/', SubmitRequestCreateView.as_view(), name='submit-request-list'),
]
