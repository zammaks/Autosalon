from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ReviewViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'revievvs', ReviewViewSet, basename='review')
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('reviews/', views.reviews_view, name='review_list'),
    path('reviews/add', views.add_review, name='add_review'),
    path('client/<int:client_id>/services/', views.client_services, name='client_services'),
    path('client/<int:client_id>/add_service/', views.add_service, name='add_service'),
    path('salons/', views.salon_list, name='salon_list'),
    path('salons/add/', views.add_salon, name='add_salon'),
    path('api/reviews/my_reviews/', ReviewViewSet.as_view({'get': 'my_reviews'}), name='my_reviews'),
] + router.urls
