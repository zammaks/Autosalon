from rest_framework import serializers
from .models import Client, Review, Service, Salon


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'execution_time', 'is_completed', 'clients']  # укажите все поля, которые вам нужны 


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'
