from django.urls import path
from apps.chat.views import *


urlpatterns = [
    path('start_convo/', StartConversationView.as_view(), name='start_convo'),
    path('get_conversation/<int:convo_id>/', GetConversationView.as_view(), name='get_conversation'),
    path('conversations/', ConversationListView.as_view(), name='conversations'),
]