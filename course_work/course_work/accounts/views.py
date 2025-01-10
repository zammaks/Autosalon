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
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Client, Review
from .serializers import ClientSerializer, ReviewSerializer
from django.db.models import Q
from .forms import ServiceFilterForm
from django.core.paginator import Paginator
from django.shortcuts import render

def reviews_view(request):
    # Получаем все отзывы, отсортированные по дате
    review_list = Review.objects.all().order_by('-created_at')

    # Создаем объект пагинации: 5 отзывов на страницу
    paginator = Paginator(review_list, 5)  # 5 отзывов на страницу

    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передаем в контекст шаблона объект пагинации
    return render(request, 'accounts/review_list.html', {'page_obj': page_obj})


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления клиентами.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]  # Только чтение для анонимов, изменение для авторизованных


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления отзывами.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]



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

# def service_list(request):
#     form = ServiceFilterForm(request.GET)
#     services = Service.objects.all()

#     if form.is_valid():
#         # Получаем фильтры из формы
#         client = form.cleaned_data.get('client')
#         min_price = form.cleaned_data.get('min_price')
#         max_price = form.cleaned_data.get('max_price')
#         max_days = form.cleaned_data.get('max_days')

#         # Формируем фильтр с использованием Q объектов
#         filter_conditions = Q()

#         if client:
#             filter_conditions &= Q(clients=client)

#         if min_price is not None:
#             filter_conditions &= Q(price__gte=min_price)

#         if max_price is not None:
#             filter_conditions &= Q(price__lte=max_price)

#         if max_days is not None:
#             filter_conditions &= Q(execution_time__lte=max_days)

#         # Применяем фильтрацию с условием OR для определенных полей
#         services = services.filter(filter_conditions)

#     return render(request, 'your_template.html', {
#         'form': form,
#         'services': services,
#     })




# def client_services(request, client_id):
#     client = get_object_or_404(Client, id=client_id)
#     services = client.services.all()  # Получаем все услуги клиента

#     if request.method == 'POST':
#         form = ClientSelectForm(request.POST)
#         if form.is_valid():
#             selected_client = form.cleaned_data['client']
#             return redirect('client_services', client_id=selected_client.id)
#     else:
#         form = ClientSelectForm(initial={'client': client})

#     context = {
#         'client': client,
#         'services': services,  # Передаем услуги в контекст
#         'form': form,  # Передаем форму в контекст
#     }
#     return render(request, 'accounts/client_services.html', context)


def client_services(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    services = client.services.all()  # Получаем все услуги клиента

    # Форма для выбора клиента и фильтрации услуг
    form = ServiceFilterForm(request.GET)
    
    # Если форма отправлена
    if form.is_valid():
        # Получаем фильтры из формы
        selected_client = form.cleaned_data.get('client')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        max_days = form.cleaned_data.get('max_days')
        name = form.cleaned_data.get('name')

        # Если выбран другой клиент, перенаправляем на его страницу
        if selected_client:
            return redirect('client_services', client_id=selected_client.id)

        # Применяем фильтрацию
        filter_conditions = Q()

        # Фильтруем по названию и описанию услуги (OR)
        if name:
            filter_conditions |= Q(name__icontains=name)  # Ищем по части названия
            filter_conditions |= Q(description__icontains=name)  # Ищем по части описания

        # Фильтруем по цене
        if min_price is not None:
            filter_conditions &= Q(price__gte=min_price)

        if max_price is not None:
            filter_conditions &= Q(price__lte=max_price)

        # Фильтруем по времени исполнения
        if max_days is not None:
            filter_conditions &= Q(execution_time__lte=max_days)

        # Применяем фильтрацию только к услугам выбранного клиента
        services = services.filter(filter_conditions)

    # Передаем данные формы и оставляем их в полях
    context = {
        'client': client,
        'services': services,
        'form': form,  # Передаем форму с данными фильтрации
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


