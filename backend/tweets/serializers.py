from rest_framework import serializers
from .models import Tweet, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class TweetAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    author = TweetAuthorSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'tweet', 'author', 'content', 'created_at']
        read_only_fields = ['tweet']

class TweetSerializer(serializers.ModelSerializer):
    author = TweetAuthorSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['id', 'author', 'content', 'created_at', 'likes_count', 'comments_count', 'is_liked']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False