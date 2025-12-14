from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()

# 1. Регистрация (ВЕРНУЛ ЭТОТ КЛАСС)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Разрешаем всем
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Хешируем пароль при создании
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

# 2. Профиль текущего пользователя (Me)
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# 3. Профиль любого пользователя
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 4. Подписка / Отписка
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself"}, status=400)
            
        request.user.following.add(user_to_follow)
        return Response({"status": "followed"})

    def delete(self, request, username):
        user_to_unfollow = get_object_or_404(User, username=username)
        request.user.following.remove(user_to_unfollow)
        return Response({"status": "unfollowed"})