from django.shortcuts import render,redirect
from .models import Announcement
from .forms import AnnouncementForm
from django.views.generic import DetailView,UpdateView,DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Announcement, FavoriteAd

def automobils_home(request):
    automobils = Announcement.objects.order_by('-date')
    return render(request,'automobils/automobils_home.html',{'automobils': automobils})


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'automobils/details_view.html'
    context_object_name = 'announcement'

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    template_name = 'automobils/announcement-update.html'
    form_class = AnnouncementForm


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