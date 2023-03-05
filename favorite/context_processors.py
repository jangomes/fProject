from .models import Favorite, FavItem
from .views import _fav_id

# It counts the number of items in a user's favorite list.
def counter(request):
    #it initializes the favorite_count variable to zero
    favorite_count = 0
    #it checks if the word 'admin' is in the request path.
    if 'admin' in request.path:
        #If it is, the function returns an empty dictionary.
        return {}
        #If not, the function tries to get the Favorite object that
        # matches the fav_id of the request.
    else:
        try:
            favorite = Favorite.objects.filter(fav_id=_fav_id(request))
            if request.user.is_authenticated:
                favorite_items = FavItem.objects.all().filter(user=request.user)
            else:
                favorite_items = FavItem.objects.all().filter(favorite=favorite[:1])
            for favorite_item in favorite_items:
                favorite_count = favorite_count + favorite_item.quantity
        except Favorite.DoesNotExist:
            favorite_count = 0
    # Here the function returns a dictionary containing the favorite_count.        
    return dict(favorite_count=favorite_count)
