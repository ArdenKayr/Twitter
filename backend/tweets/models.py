from django.db import models
from django.conf import settings

class Tweet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_tweets', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author}: {self.content[:20]}..."

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Комментарии идут по порядку: сначала старые

    def __str__(self):
        return f"Comment by {self.author} on {self.tweet}"