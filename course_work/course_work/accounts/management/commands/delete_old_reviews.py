from django.core.management.base import BaseCommand
from accounts.models import Review

class Command(BaseCommand):
    help = 'Удаляет самые старые 5 отзывов из базы данных'

    def handle(self, *args, **kwargs):
        # Получаем 5 самых старых отзывов
        oldest_reviews = Review.objects.order_by('created_at')[:5]

        # Сохраняем количество отзывов для отчета
        count = oldest_reviews.count()

        if count == 0:
            self.stdout.write(self.style.WARNING('Нет отзывов для удаления.'))
        else:
            # Удаляем отзывы по одному
            for review in oldest_reviews:
                review.delete()

            self.stdout.write(self.style.SUCCESS(f'Удалено {count} старых отзывов.'))
