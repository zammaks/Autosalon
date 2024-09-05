from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.shortcuts import render, get_object_or_404
from .models import Client
from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Service
from .forms import ServiceForm, ClientSelectForm
from .models import Salon
from .forms import SalonForm, CitySelectForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Обновите 'home' на правильный URL
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('home')




def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'accounts/review_list.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'accounts/add_review.html', {'form': form})








# def client_services(request, client_id):
#     client = get_object_or_404(Client, id=client_id)
#     services = client.services.all()  # Получаем все услуги клиента

#     context = {
#         'client': client,
#         'services': services,  # Передаем услуги в контекст
#     }
#     return render(request, 'accounts/client_services.html', context)






# def add_service(request, client_id):
#     client = get_object_or_404(Client, id=client_id)

#     if request.method == 'POST':
#         form = ServiceForm(request.POST)
#         if form.is_valid():
#             service = form.save(commit=False)
#             service.save()
#             client.services.add(service)
#             return redirect('client_services', client_id=client.id)
#     else:
#         form = ServiceForm()

#     context = {
#         'client': client,
#         'form': form,
#     }
#     return render(request, 'accounts/add_service.html', context)






def client_services(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    services = client.services.all()  # Получаем все услуги клиента

    if request.method == 'POST':
        form = ClientSelectForm(request.POST)
        if form.is_valid():
            selected_client = form.cleaned_data['client']
            return redirect('client_services', client_id=selected_client.id)
    else:
        form = ClientSelectForm(initial={'client': client})

    context = {
        'client': client,
        'services': services,  # Передаем услуги в контекст
        'form': form,  # Передаем форму в контекст
    }
    return render(request, 'accounts/client_services.html', context)

def add_service(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            client.services.add(service)
            return redirect('client_services', client_id=client.id)
    else:
        form = ServiceForm()

    context = {
        'client': client,
        'form': form,
    }
    return render(request, 'accounts/add_service.html', context)





def salon_list(request):
    city = request.GET.get('city')
    if city:
        salons = Salon.objects.filter(city=city)
    else:
        salons = Salon.objects.all()

    form = CitySelectForm(initial={'city': city})

    context = {
        'salons': salons,
        'form': form,
    }
    return render(request, 'accounts/salon_list.html', context)

def add_salon(request):
    if request.method == 'POST':
        form = SalonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_list')
    else:
        form = SalonForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/add_salon.html', context)