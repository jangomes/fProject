from django.contrib import admin
from .models import Favorite, FavItem
# Register your models here.

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('fav_id', 'date_added')

class FavoriteItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'favorite', 'quantity', 'is_active')

admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(FavItem, FavoriteItemAdmin)

#
