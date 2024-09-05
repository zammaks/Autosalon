from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('reviews', views.review_list, name='review_list'),
    path('reviews/add', views.add_review, name='add_review'),
    path('client/<int:client_id>/services/', views.client_services, name='client_services'),
    path('client/<int:client_id>/add_service/', views.add_service, name='add_service'),
    path('salons/', views.salon_list, name='salon_list'),
    path('salons/add/', views.add_salon, name='add_salon'),

]
