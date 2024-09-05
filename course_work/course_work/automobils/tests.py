from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Announcement, FavoriteAd
from django.utils import timezone

class AnnouncementModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.announcement = Announcement.objects.create(
            title='Toyota',
            image=None,
            model='Camry',
            color='Black',
            fabrication='2020-01-01',
            mileage=10000,
            price=2000000,
            full_text='A well-maintained car',
            date=timezone.now()
        )

    def test_announcement_str(self):
        self.assertEqual(str(self.announcement), 'Toyota')

    def test_get_absolute_url(self):
        self.assertEqual(self.announcement.get_absolute_url(), f'/automobils/{self.announcement.id}')

    def test_is_favorite_for_user(self):
        FavoriteAd.objects.create(user=self.user, announcement=self.announcement)
        self.assertTrue(self.announcement.is_favorite_for_user(self.user))

    def test_toggle_favorite(self):
        # Initially not favorite
        self.assertFalse(self.announcement.is_favorite_for_user(self.user))
        
        # Toggle to favorite
        self.assertTrue(self.announcement.toggle_favorite(self.user))
        self.assertTrue(self.announcement.is_favorite_for_user(self.user))
        
        # Toggle off from favorite
        self.assertFalse(self.announcement.toggle_favorite(self.user))
        self.assertFalse(self.announcement.is_favorite_for_user(self.user))

class FavoriteAdModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.announcement = Announcement.objects.create(
            title='Toyota',
            image=None,
            model='Camry',
            color='Black',
            fabrication='2020-01-01',
            mileage=10000,
            price=2000000,
            full_text='A well-maintained car',
            date=timezone.now()
        )
        self.favorite_ad = FavoriteAd.objects.create(user=self.user, announcement=self.announcement)

    def test_favorite_ad_str(self):
        self.assertEqual(str(self.favorite_ad), f'{self.user.username} - {self.announcement.title}')

    def test_unique_together(self):
        # Trying to create another FavoriteAd with the same user and announcement should fail
        with self.assertRaises(IntegrityError):
            FavoriteAd.objects.create(user=self.user, announcement=self.announcement)
