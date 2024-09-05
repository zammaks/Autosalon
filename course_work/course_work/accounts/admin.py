from django.contrib import admin
from .models import Client, Review, Service, Salon


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

# Регистрируем инлайн модель для отзывов отдельно или внутри модели, если необходимо
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'text', 'author__username')
    raw_id_fields = ('author',)
    readonly_fields = ('created_at',)

# Можно добавить инлайны в нужные модели, если необходимо
class ClientInline(admin.TabularInline):
    model = Client.services.through
    extra = 1

# Вставляем инлайн в Service
ServiceAdmin.inlines = [ClientInline]
