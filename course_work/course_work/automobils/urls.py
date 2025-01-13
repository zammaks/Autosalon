from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.automobils_home, name='auto'),
    path('api/', include('automobils.urls_api')),  # Маршруты API
    path('create', views.create, name='create'),
    path('<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('<int:pk>/update', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('<int:pk>/delete', views.AnnouncementDeleteView.as_view(), name='announcement-delete'),

    path('', views.automobils_home, name='automobils-home'),
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('<int:pk>/', views.AnnouncementDetailView.as_view(), name='automobil-detail'),
    path('announcement/<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcement/<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('announcement/create/', views.create, name='announcement-create'),
    path('announcement/<int:pk>/add_to_favorites/', views.add_to_favorites, name='add-to-favorites'),
    path('favorites/', views.favorites_list, name='favorites-list'),
    path('favorites/', views.favorites_list, name='favorites-list'),
    path('favorites/delete/', views.favorites_delete, name='favorites-delete'),

]



