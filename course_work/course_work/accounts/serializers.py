from rest_framework import serializers
from .models import Client, Review, Service, Salon


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # Вы можете указать только нужные поля, например: ['id', 'user', 'phone_number', 'first_name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # Аналогично, здесь можно указать только важные поля


class ServiceSerializer(serializers.ModelSerializer):
    # Чтобы отображать связанных клиентов (многие-ко-многим) в удобном формате:
    clients = ClientSerializer(many=True, read_only=True)  

    class Meta:
        model = Service
        fields = '__all__'


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'
