from django.urls import path
from .views import ConversationListView, ConversationDetailView, StartChatView

urlpatterns = [
    # Список всех чатов
    path('conversations/', ConversationListView.as_view(), name='conversations-list'),
    
    # Начать чат с кем-то (по username)
    path('conversations/start/<str:username>/', StartChatView.as_view(), name='start-chat'),
    
    # Сообщения внутри конкретного чата (по ID диалога)
    path('conversations/<int:pk>/messages/', ConversationDetailView.as_view(), name='conversation-messages'),
]