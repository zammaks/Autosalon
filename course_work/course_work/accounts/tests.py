from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client, Review, Service, Salon
from django.utils import timezone

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='12345')
        self.client = Client.objects.create(
            user=self.user,
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            birth_date=timezone.now().date(),
            gender='M'
        )

    def test_client_creation(self):
        self.assertTrue(isinstance(self.client, Client))
        self.assertEqual(self.client.__str__(), 'John Doe')
        self.assertEqual(self.client.phone_number, '1234567890')

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='reviewer', password='12345')
        self.review = Review.objects.create(
            title='Great Service',
            text='The service was excellent.',
            author=self.user,
        )

    def test_review_creation(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.__str__(), 'Great Service')
        self.assertEqual(self.review.text, 'The service was excellent.')

class ServiceModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Haircut',
            description='A basic haircut service.',
            price=15.00,
            execution_time=1
        )

    def test_service_creation(self):
        self.assertTrue(isinstance(self.service, Service))
        self.assertEqual(self.service.__str__(), 'Haircut')
        self.assertEqual(self.service.price, 15.00)

class SalonModelTest(TestCase):
    def setUp(self):
        self.salon = Salon.objects.create(
            city='New York',
            address='123 Broadway',
            phone='123-456-7890',
            email='contact@salon.com',
            telegram='@salon'
        )

    def test_salon_creation(self):
        self.assertTrue(isinstance(self.salon, Salon))
        self.assertEqual(self.salon.__str__(), 'New York - 123 Broadway')
        self.assertEqual(self.salon.email, 'contact@salon.com')
