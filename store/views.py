from django.shortcuts import render, get_object_or_404
from .models import Product, ProductGallery
from category.models import Category
from favorite.models import FavItem
from favorite.views import _fav_id
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.

# It handles requests for displaying products in the store.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_favorite = FavItem.objects.filter(favorite__fav_id=_fav_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    #product gallery

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)


    context = {
        'single_product': single_product,
        'in_favorite' : in_favorite,
        'product_gallery' : product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    # The search() function is defined to handle search requests from the user.
    # The function checks if the 'keyword' parameter is present in the GET request.
    # If the 'keyword' parameter is present, the function gets the keyword value from the GET
    # request and uses it to filter the Products model by matching the keyword with the
    # description or the product name field using the icontains operator.
    #The function then creates a context dictionary with the filtered products and renders the
    #'store.html' template with the context.
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |  Q(product_name__icontains=keyword))
            product_count = products.count()




    context = {
        'products' : products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
