from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода данных о пользователе"""
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'date_joined', 'followers_count', 'following_count', 'is_following']
        read_only_fields = ['date_joined', 'followers_count', 'following_count', 'is_following']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_is_following(self, obj):
        # Проверяем, подписан ли текущий пользователь (кто делает запрос) на этого юзера
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор только для регистрации (создания)"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name']

    def create(self, validated_data):
        # Используем create_user, чтобы пароль правильно захэшировался
        user = User.objects.create_user(**validated_data)
        return user