from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Tweet, Comment
from .serializers import TweetSerializer, CommentSerializer

class TweetListCreateView(generics.ListCreateAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Tweet.objects.all()
        
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(author__username=username)

        feed_type = self.request.query_params.get('feed_type')
        if feed_type == 'following' and self.request.user.is_authenticated:
            queryset = queryset.filter(author__followers=self.request.user)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TweetDetailView(generics.RetrieveDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You cannot delete this tweet")
        instance.delete()

class TweetLikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        
        if tweet.likes.filter(id=request.user.id).exists():
            tweet.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            tweet.likes.add(request.user)
            return Response({'status': 'liked'})

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        tweet_id = self.kwargs['tweet_pk']
        return Comment.objects.filter(tweet_id=tweet_id)

    def perform_create(self, serializer):
        tweet = get_object_or_404(Tweet, pk=self.kwargs['tweet_pk'])
        serializer.save(author=self.request.user, tweet=tweet)