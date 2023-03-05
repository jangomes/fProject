from django.contrib import admin
from .models import Pedido, Order, OrderProduct
# Register your models here.

admin.site.register(Pedido)
admin.site.register(Order)
admin.site.register(OrderProduct)
