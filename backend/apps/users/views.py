from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, RegistrationSerializer

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    permission_classes = [AllowAny] # Разрешено всем (даже без токена)
    serializer_class = RegistrationSerializer

class MeView(generics.RetrieveAPIView):
    """Получить данные своего профиля"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserProfileView(generics.RetrieveAPIView):
    """Получить данные профиля любого пользователя по username"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username' # Ищем по username, а не по id

class FollowUserView(views.APIView):
    """Подписаться / Отписаться"""
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        if target_user == request.user:
            return Response({"error": "Нельзя подписаться на самого себя"}, status=400)
        
        request.user.following.add(target_user)
        return Response({"status": "followed"})

    def delete(self, request, username):
        target_user = get_object_or_404(User, username=username)
        request.user.following.remove(target_user)
        return Response({"status": "unfollowed"})