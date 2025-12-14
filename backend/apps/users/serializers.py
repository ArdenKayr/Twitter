# ================================================
# FILE: backend/apps/users/serializers.py (Создать)
# ================================================
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Добавляем поля для чтения
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    # ВАЖНО: Аватар и Био
    avatar = serializers.ImageField(read_only=True) # Пока только чтение, загрузку сделаем отдельно
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'bio', 'avatar',  # <--- Не забудьте добавить сюда
            'followers_count', 'following_count', 'is_following'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового пользователя (регистрации)."""
    # Пароль должен быть только для записи и не выводиться в ответе API.
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name']
    
    # Переопределяем метод create для правильного хэширования пароля.
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user