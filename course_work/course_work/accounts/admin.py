from django.contrib import admin
from .models import Client, Review, Service, Salon
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ExportMixin
from django.http import HttpResponse



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'first_name', 'last_name', 'gender', 'created_at', 'full_name')
    list_filter = ('gender', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('first_name', 'last_name', 'phone_number', 'user__username')
    list_display_links = ('user', 'first_name', 'last_name')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at',)

    @admin.display(description='Полное имя')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'execution_time', 'client_count')
    search_fields = ('name', 'description')
    filter_horizontal = ('clients',)

    @admin.display(description='Количество клиентов')
    def client_count(self, obj):
        return obj.clients.count()


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'phone', 'email')
    search_fields = ('city', 'address', 'phone', 'email')
    list_filter = ('city',)



# Создайте ресурс для модели, чтобы управлять экспортом
class ReviewResource(resources.ModelResource):
    # Кастомизация поля title
    def dehydrate_title(self, review):
        """
        Возвращает заголовок в формате 'Title: {название}'.
        Зачем: Добавляет префикс для визуальной идентификации данных в экспортированном файле.
        """
        return f"Title: {review.title}"

    # Кастомизация поля author
    def dehydrate_author(self, review):
        """
        Возвращает имя автора в формате 'Author: {имя автора}'.
        Зачем: Обеспечивает ясность в случае, если поле "автор" будет использоваться для обработки данных.
        """
        return f"Author: {review.author.username}"

    # Кастомизация даты создания
    def dehydrate_created_at(self, review):
        """
        Возвращает дату создания в удобном для экспорта формате (YYYY-MM-DD HH:MM).
        Зачем: Форматирование даты для облегчения чтения в Excel.
        """
        return review.created_at.strftime('%Y-%m-%d %H:%M')

    # Кастомизация текста отзыва
    def dehydrate_text(self, review):
        """
        Обрезает текст отзыва до 100 символов и добавляет '...' для длинных отзывов.
        Зачем: Сохраняет читаемость файла, чтобы длинные тексты не занимали слишком много места.
        """
        return review.text[:100] + ('...' if len(review.text) > 100 else '')

    class Meta:
        model = Review
        fields = ('title', 'author', 'created_at', 'text')  # Поля, которые будут экспортироваться
        export_order = ('title', 'author', 'created_at', 'text')  # Упорядочивание столбцов в экспорте

    # Можно добавить больше кастомных методов для других полей по аналогии

# Регистрируем инлайн модель для отзывов отдельно или внутри модели, если необходимо
@admin.register(Review)
class ReviewAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReviewResource

    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'text', 'author__username')
    raw_id_fields = ('author',)
    readonly_fields = ('created_at',)
    history_list_display = ('history_user', 'history_date', 'history_type')

    # Определяем действия в админке, такие как экспорт в Excel
    actions = ['export_as_excel']

    def export_as_excel(self, request, queryset):
        """
        Экспорт выбранных отзывов в формате Excel.
        """
        resource = self.resource_class()
        dataset = resource.export(queryset=queryset)  # Получаем набор данных для экспорта
        response = HttpResponse(
            dataset.export('xlsx'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="reviews_export.xlsx"'
        return response

    def get_export_queryset(self, request):
        """
        Этот метод гарантирует, что мы экспортируем правильные данные.
        Если необходимо, можно фильтровать данные.
        """
        return Review.objects.all()

    # Дополнительный кастомизированный метод для обработки текста
    def get_text_summary(self, obj):
        """
        Возвращает обрезанный текст отзыва для отображения в админке.
        Зачем: Чтобы текст не занимал слишком много места в списке объектов.
        """
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')

    get_text_summary.short_description = "Краткий текст"



# Можно добавить инлайны в нужные модели, если необходимо
class ClientInline(admin.TabularInline):
    model = Client.services.through
    extra = 1

# Вставляем инлайн в Service
ServiceAdmin.inlines = [ClientInline]
