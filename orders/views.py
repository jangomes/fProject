from django.shortcuts import render, redirect
from favorite.models import FavItem
from .forms import OrderForm
import datetime
from .models import Order
from django.http import HttpResponse

# The view function that allows users to place an order after adding items to their favorites.

def place_detail(request):
    current_user = request.user
# It gets the current user and retrieves their favorite items from the FavItem model.
    favorite_items = FavItem.objects.filter(user=current_user)
    favorite_count = favorite_items.count()
    if favorite_count <= 0:
        return redirect('store')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store inf inside the table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.order_note = form.cleaned_data['order_note']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Genarate order order_number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str (data.id)
            data.order_number = order_number
            data.save()
            return redirect('senddetails')
        else:
            return redirect('senddetails')
    else:
        return redirect('senddetails')
# If the form is not valid, or the request method is not POST, the function redirects the user to the senddetails view
