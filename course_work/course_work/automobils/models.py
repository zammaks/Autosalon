from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Announcement(models.Model):
    title = models.CharField('Бренд', max_length=50)
    image = models.FileField('Фото автомобиля', upload_to='automobils/static/automobils/img', null=True, blank=True)
    model = models.CharField('Модель', max_length=50)
    color = models.CharField('Цвет', max_length=50)
    fabrication = models.DateField('Год выпуска')
    mileage = models.IntegerField('Пробег, км')
    price = models.IntegerField('Цена, р')
    full_text = models.TextField('Описание')
    date = models.DateTimeField('Дата публикации', default=timezone.now)

    def is_favorite_for_user(self, user):
        return self.favoritead_set.filter(user=user).exists()

    def toggle_favorite(self, user):
        if self.is_favorite_for_user(user):
            self.favoritead_set.filter(user=user).delete()
            return False
        else:
            FavoriteAd.objects.create(announcement=self, user=user)
            return True

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/automobils/{self.id}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class FavoriteAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'announcement')

    def __str__(self):
        return f"{self.user.username} - {self.announcement.title}"
