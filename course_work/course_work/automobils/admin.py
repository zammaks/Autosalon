from django.contrib import admin
from .models import Announcement, FavoriteAd



from django.contrib import admin
from .models import Announcement, FavoriteAd

class FavoriteAdInline(admin.TabularInline):
    model = FavoriteAd
    extra = 1

@admin.display(description='Price (in rubles)')
def display_price(obj):
    return f"{obj.price} р"

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'color', 'fabrication', 'mileage', display_price, 'date', 'is_favorite')
    list_filter = ('color', 'fabrication', 'price')
    inlines = [FavoriteAdInline]
    date_hierarchy = 'date'
    search_fields = ('title', 'model', 'color', 'full_text')
    list_display_links = ('title', 'model')
    readonly_fields = ('date', 'is_favorite')

    def is_favorite(self, obj):
        # Example: Return True if the object has any associated FavoriteAd entries
        return obj.favoritead_set.exists()
    is_favorite.short_description = 'Favorite'
    is_favorite.boolean = True

class FavoriteAdAdmin(admin.ModelAdmin):
    list_display = ('user', 'announcement', 'date_added')
    search_fields = ('user__username', 'announcement__title')
    raw_id_fields = ('user', 'announcement')

admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(FavoriteAd, FavoriteAdAdmin)
