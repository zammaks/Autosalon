from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Client(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, verbose_name="Телефон", null=True)
    first_name = models.CharField(max_length=128, verbose_name="Имя", null=True)
    last_name = models.CharField(max_length=128, verbose_name="Фамилия", null=True)
    second_name = models.CharField(max_length=128, verbose_name="Отчество", null=True, blank=True)
    birth_date = models.DateField(null=True, verbose_name="Дата рождения", blank=True)
    gender = models.CharField(max_length=1, verbose_name="Пол", choices=GENDER_CHOICES, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        first_name = self.first_name if self.first_name else ''
        last_name = self.last_name if self.last_name else ''
        full_name = f'{first_name} {last_name}'.strip()
        return full_name


class Review(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время добавления")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.title
    

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена услуги")
    execution_time = models.IntegerField(verbose_name="Время исполнения (в днях)")
    clients = models.ManyToManyField(Client, related_name='services', verbose_name="Клиенты")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Salon(models.Model):
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    telegram = models.CharField(max_length=50, verbose_name="Телеграм")

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"

    def __str__(self):
        return f"{self.city} - {self.address}"
