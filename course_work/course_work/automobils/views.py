from django.shortcuts import render,redirect
from .models import Announcement
from .forms import AnnouncementForm
from django.views.generic import DetailView,UpdateView,DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Announcement, FavoriteAd
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Announcement
from .serializers import AnnouncementSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import FavoriteAd


def automobils_home(request):
    automobils = Announcement.objects.order_by('-date')
    
    brand = request.GET.get('brand')
    model = request.GET.get('model')

    if brand:
        automobils = automobils.filter(title=brand)

    if model:
        automobils = automobils.filter(model=model)

    brands = Announcement.objects.values_list('title', flat=True).distinct()
    models = Announcement.objects.values_list('model', flat=True).distinct()

    context = {
        'automobils': automobils,
        'brands': brands,
        'models': models,
        'selected_brand': brand,
        'selected_model': model,
    }
    return render(request, 'automobils/automobils_home.html', context)


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'automobils/details_view.html'
    context_object_name = 'announcement'

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    template_name = 'automobils/announcement-update.html'
    form_class = AnnouncementForm

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API для работы с объявлениями:
    - Получение списка объектов
    - Получение одного объекта
    - Создание, обновление и удаление объектов
    """
    queryset = Announcement.objects.all().order_by('-date')
    serializer_class = AnnouncementSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    success_url = '/automobils/'
    context_object_name = 'announcement'
    template_name = 'automobils/announcement-delete.html'

def create(request):
    error = ''
    if request.method == 'POST':
        form = AnnouncementForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/automobils/')
        else:
            error = 'Неверное заполнение формы!'


    form = AnnouncementForm()

    data = {
        'form':form,
        'error':error
    }

    return render(request,'automobils/create.html', data)




@login_required
def add_to_favorites(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    favorite, created = FavoriteAd.objects.get_or_create(user=request.user, announcement=announcement)
    if created:
        # Если объявление было добавлено в избранное
        return redirect('announcement-detail', pk=pk)
    else:
        # Если объявление уже было в избранном
        return redirect('announcement-detail', pk=pk)

@login_required
def favorites_list(request):
    favorite_ads = FavoriteAd.objects.filter(user=request.user)
    
    if request.method == 'POST':
        favorite_ad_id = request.POST.get('favorite_ad_id')
        favorite_ad = get_object_or_404(FavoriteAd, id=favorite_ad_id, user=request.user)
        favorite_ad.delete()
        return redirect('favorites-list')
    
    return render(request, 'automobils/favorites_list.html', {'favorite_ads': favorite_ads})

def favorites_delete(request):
    if request.method == 'POST':
        favorite_ad_id = request.POST.get('favorite_ad_id')
        favorite_ad = get_object_or_404(FavoriteAd, id=favorite_ad_id, user=request.user)
        favorite_ad.delete()
        return redirect('favorites-list')
    else:
        return redirect('favorites-list')  