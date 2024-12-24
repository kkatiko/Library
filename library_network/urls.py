from django.contrib import admin  # Добавляем импорт
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls')),  # Подключаем маршруты приложения
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
