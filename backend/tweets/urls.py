from django.urls import path
from .views import TweetListCreateView, TweetDetailView, TweetLikeView, CommentListCreateView

urlpatterns = [
    path('tweets/', TweetListCreateView.as_view(), name='tweet-list'),
    path('tweets/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweets/<int:pk>/like/', TweetLikeView.as_view(), name='tweet-like'),
    path('tweets/<int:tweet_pk>/comments/', CommentListCreateView.as_view(), name='tweet-comments'),
]