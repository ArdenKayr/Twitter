from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()

# 1. Список диалогов пользователя
class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только те диалоги, где участвует текущий юзер
        return self.request.user.conversations.all().order_by('-created_at')

# 2. Получить сообщения диалога / Написать сообщение
class ConversationDetailView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['pk']
        # Проверяем, что юзер участник этого диалога, чтобы не читал чужое
        return Message.objects.filter(
            conversation_id=conversation_id, 
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        conversation = get_object_or_404(Conversation, pk=self.kwargs['pk'])
        # Проверка безопасности: нельзя писать в чат, если ты не участник
        if self.request.user not in conversation.participants.all():
             raise permissions.PermissionDenied("Вы не участник этого чата")
        
        serializer.save(sender=self.request.user, conversation=conversation)

# 3. Начать чат с пользователем (создать или найти существующий)
class StartChatView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        target_user = get_object_or_404(User, username=username)
        
        if target_user == request.user:
            return Response({"error": "Нельзя писать самому себе"}, status=400)

        # Пытаемся найти существующий диалог между этими двумя
        # Логика: диалог, где есть Я и ОН, и всего 2 участника
        conversation = Conversation.objects.filter(participants=request.user)\
            .filter(participants=target_user).first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, target_user)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)