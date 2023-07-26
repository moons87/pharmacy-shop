from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Category
from carts.models import CartItem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import Paginator
from transliterate import translit
from orders.models import OrderProduct
from pharmacy.models import Pharmacy, PharmacyProductPrice
from django.db.models import Min

# Create your views here.
def sort_products(request, products):
    sort = request.GET.get('sort')
    if sort == 'asc':
        products = products.order_by('price')
    elif sort == 'desc':
        products = products.order_by('-price')
    return products

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    products = sort_products(request, products)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)   
    product_count = products.count()
    for product in products:
        pharmacy_prices = product.pharmacyproductprice_set.all().aggregate(min_price=Min('price'))
        product.min_price = pharmacy_prices['min_price']
    context = {
        'products': paged_products,
        'product_count': product_count,
        'min_price' : pharmacy_prices['min_price'] or None,
    }

    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    

    if request.user.is_authenticated:
      try:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
      except OrderProduct.DoesNotExist:
        orderproduct = None
    
    else:
        orderproduct = None
    
    

    pharmacy_prices = single_product.pharmacyproductprice_set.all().aggregate(min_price=Min('price'))
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct'  : orderproduct,
        'pharmacy_prices' : pharmacy_prices,
        'min_price' : pharmacy_prices['min_price'] or None
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = []
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            keyword_latin = translit(keyword, 'ru', reversed=True)
            
            products = Product.objects.order_by('-created_data').filter(
                Q(description__icontains=keyword) | 
                Q(product_name__icontains=keyword) |
                Q(description__icontains=keyword_latin) | 
                Q(product_name__icontains=keyword_latin)
            )
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)



    
    