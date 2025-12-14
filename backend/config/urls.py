from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ВАЖНО: Мы указываем путь через 'apps.', так как папка users лежит внутри apps
    path('api/users/', include('apps.users.urls')),
    
    path('api/', include('tweets.urls')),
    path('api/chat/', include('chat.urls')),
]

# Настройка для раздачи загруженных картинок (аватарок)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)