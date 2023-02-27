from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Favorite, FavItem

from django.http import HttpResponse

def _fav_id(request):
    favorite = request.session.session_key
    if not favorite:
        favorite = request.session.create()
    return favorite



def add_favorite(request, product_id):
    product = Product.objects.get(id=product_id) #get product

    try:
        favorite = Favorite.objects.get(fav_id=_fav_id(request))#get cart using the cart id present in the sessions
    except Favorite.DoesNotExist:
        favorite = Favorite.objects.create(
            fav_id =_fav_id(request)
        )

        favorite.save()

    #is_favorite_item_exists = FavItem.objects.filter(product=product, favorite=favorite).exists()
    #if is_favorite_item_exists:
        #favorite_item = FavItem.objects.filter(product=product, favorite=favorite)
    try:

        favorite_item = FavItem.objects.get(product=product, favorite=favorite)
        favorite_item.quantity += 1
        favorite_item.save()

    #else:
    except FavItem.DoesNotExist:
        favorite_item = FavItem.objects.create(
            product = product,
            quantity = 1,
            favorite = favorite,
        )

        favorite_item.save()

    return redirect('favorite')

def remove_favorite(request, product_id):
    favorite = Favorite.objects.get(fav_id=_fav_id(request))
    product = get_object_or_404(Product, id=product_id)
    favorite_item = FavItem.objects.get(product=product, favorite=favorite)
    if favorite_item.quantity > 1:
        favorite_item.quantity -= 1
        favorite_item.save()
    else:
        favorite_item.delete()
    return redirect('favorite')

def remove_favorite_item(request, product_id):
    favorite = Favorite.objects.get(fav_id=_fav_id(request))
    product = get_object_or_404(Product, id=product_id)
    favorite_item = FavItem.objects.get(product=product, favorite=favorite)
    favorite_item.delete()
    return redirect('favorite')

def favorite(request, total=0, quantity=0, favorite_items=None):
    try:
        favorite = Favorite.objects.get(fav_id=_fav_id(request))
        favorite_items = FavItem.objects.filter(favorite=favorite, is_active=True)
        for favorite_item in favorite_items:
            #dont need price
            quantity += favorite_item.quantity

    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'favorite_items': favorite_items,
    }


    return render(request, 'store/favorite.html', context)

def senddetails(request, total=0, quantity=0, favorite_items=None):
    try:
        favorite = Favorite.objects.get(fav_id=_fav_id(request))
        favorite_items = FavItem.objects.filter(favorite=favorite, is_active=True)
        for favorite_item in favorite_items:
            #dont need price
            quantity += favorite_item.quantity

    except FavItem.DoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'favorite_items': favorite_items,
    }
    return render(request, 'store/senddetails.html', context)
