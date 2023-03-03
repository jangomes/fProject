from .models import Favorite, FavItem
from .views import _fav_id

def counter(request):
    favorite_count = 0
    if 'admin' in request.path:
        return {}
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
    return dict(favorite_count=favorite_count)
