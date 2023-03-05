#from django import favorite_items
from django import forms # added from code
from favorite.models import FavItem # added from code
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'order_note']
