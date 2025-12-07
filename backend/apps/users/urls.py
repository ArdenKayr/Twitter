from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistrationView, MeView, UserProfileView, FollowUserView

urlpatterns = [
    # Авторизация (JWT)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Вход (Login)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Обновление токена
    
    # Пользователи
    path('register/', RegistrationView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    path('<str:username>/', UserProfileView.as_view(), name='profile'),
    path('<str:username>/follow/', FollowUserView.as_view(), name='follow'),
]