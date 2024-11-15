from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshSlidingView

from apps.account.views import *

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', CustomAuthTokenView.as_view(), name='signin'),
    path('roles/', RoleListView.as_view(), name='roles'),
    path('user/', CustomUserDetailView.as_view(), name='user-detail'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
    path('user/statics/', StatisticsCustomUserView.as_view(), name='statics-user'),
    path('custom-user-filters/', CustomUserFilterAPIView.as_view(), name='custom_user_filters'),
    path('token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
]