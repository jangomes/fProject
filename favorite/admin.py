from django.contrib import admin
from .models import Favorite, FavItem
# Register your models here.

admin.site.register(Favorite)
admin.site.register(FavItem)
