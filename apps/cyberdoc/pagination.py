from rest_framework import pagination


class OrderWorkPagination(pagination.PageNumberPagination):
    page_size = 10  # Define the number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100
