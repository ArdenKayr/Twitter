from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, UserDetailView, MeView, FollowUserView

urlpatterns = [
    # Авторизация (Токены)
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Профили
    path('me/', MeView.as_view(), name='current-user'),
    path('<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('<str:username>/follow/', FollowUserView.as_view(), name='user-follow'),
]