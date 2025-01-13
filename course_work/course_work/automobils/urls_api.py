from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet

# Создаем маршрутизатор
router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
]
