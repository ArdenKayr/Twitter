from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

# Простой сериализатор пользователя для чата
class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = ChatUserSerializer(read_only=True)
    
    # ВАЖНО: Добавляем эту строку, чтобы исправить ошибку 400
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = ChatUserSerializer(many=True, read_only=True)
    
    # Чтобы на фронтенде удобно получать последнее сообщение (для превью в списке)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None