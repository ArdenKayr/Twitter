from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Все URL, начинающиеся с api/users/, пойдут в наше приложение users
    path('api/users/', include('apps.users.urls')),
]