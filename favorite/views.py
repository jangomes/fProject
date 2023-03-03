from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Favorite, FavItem
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def _fav_id(request):
    favorite = request.session.session_key
    if not favorite:
        favorite = request.session.create()
    return favorite



def add_favorite(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get product
# when the user is is authenticated this code is going
#to be used in the if or else condition
    if current_user.is_authenticated:

        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                    key = item
                    value = request.POST[key]

                    try:
                        variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                        product_variation.append(variation)
                    except:
                        pass

        is_favorite_item_exists = FavItem.objects.filter(product=product, user=current_user).exists()
        if is_favorite_item_exists:
            favorite_item = FavItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in favorite_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            #this part of the code is going to increase the product
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = FavItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()

            else:
            # in here we create the new
                item = FavItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
#when the user is not authenticated we are going to use this code for the
# else condition
        else:
            favorite_item = FavItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                favorite_item.variations.clear()
                favorite_item.variations.add(*product_variation)

            favorite_item.save()

        return redirect('favorite')

    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                    key = item
                    value = request.POST[key]

                    try:
                        variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                        product_variation.append(variation)
                    except:
                        pass


        try:
            favorite = Favorite.objects.get(fav_id=_fav_id(request))
            #get favorite using the favorite id present in the sessions
        except Favorite.DoesNotExist:
            favorite = Favorite.objects.create(
                fav_id =_fav_id(request)
            )

            favorite.save()

        is_favorite_item_exists = FavItem.objects.filter(product=product, favorite=favorite).exists()
        if is_favorite_item_exists:
            favorite_item = FavItem.objects.filter(product=product, favorite=favorite)
            #in here we verify if the current product already exists inside
            #the card with the same variations if yes we only add to the existing one
            #if not we create a new product at the fav
            ex_var_list = []
            id = []
            for item in favorite_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            #this part of the code is going to increase the product
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = FavItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()

            else:
            # in here we create the new
                item = FavItem.objects.create(product=product, quantity=1, favorite=favorite)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()

        else:
            favorite_item = FavItem.objects.create(
                product = product,
                quantity = 1,
                favorite = favorite,
            )
            if len(product_variation) > 0:
                favorite_item.variations.clear()
                favorite_item.variations.add(*product_variation)

            favorite_item.save()

        return redirect('favorite')

def remove_favorite(request, product_id, favorite_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            favorite_item = FavItem.objects.get(product=product, user=request.user, id=favorite_item_id)
        else:
            favorite = Favorite.objects.get(fav_id=_fav_id(request))
            favorite_item = FavItem.objects.get(product=product, favorite=favorite, id=favorite_item_id)
        if favorite_item.quantity > 1:
            favorite_item.quantity -= 1
            favorite_item.save()
        else:
            favorite_item.delete()
    except:
        pass
    return redirect('favorite')

def remove_favorite_item(request, product_id, favorite_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        favorite_item = FavItem.objects.get(product=product, user=request.user, id=favorite_item_id)
    else:
        favorite = Favorite.objects.get(fav_id=_fav_id(request))
        favorite_item = FavItem.objects.get(product=product, favorite=favorite, id=favorite_item_id)
    favorite_item.delete()
    return redirect('favorite')

def favorite(request, total=0, quantity=0, favorite_items=None):
    try:
        if request.user.is_authenticated:
            favorite_items = FavItem.objects.filter(user=request.user, is_active=True)
        else:
            favorite = Favorite.objects.get(fav_id=_fav_id(request))
            favorite_items = FavItem.objects.filter(favorite=favorite, is_active=True)
        for favorite_item in favorite_items:
            quantity += favorite_item.quantity

    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'favorite_items': favorite_items,
    }


    return render(request, 'store/favorite.html', context)


@login_required(login_url='login')
def senddetails(request, total=0, quantity=0, favorite_items=None):
    try:
        if request.user.is_authenticated:
            favorite_items = FavItem.objects.filter(user=request.user, is_active=True)
        else:
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
