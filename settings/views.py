from django.shortcuts import render
from django.db.models import Count
from product.models import Product , Brand , Review
#from django.views.decorators.cache import cache_page




#@cache_page(60 * 60 * 24)
def home(request):
    brands = Brand.objects.all().annotate(product_count=Count('product_brand'))
    sale_products = Product.objects.filter(flag='Sale')[:10]
    feature_products = Product.objects.filter(flag='Feature')[:6]
    new_products = Product.objects.filter(flag='New')[:10]
    reviews = Review.objects.all()[:5]
    #browse by top niche 
    top_order_products = Product.objects.order_by('-order_count')[:10]
    top_rating_products = Product.objects.order_by('-rating')[:10]
    top_discount_products = Product.objects.order_by('-discount')[:10]

    return render(request,'settings/home.html',{
        'brands':brands ,
        'sale_products':sale_products ,
        'feature_products':feature_products ,
        'new_products':new_products ,
        'reviews':reviews ,

        'top_order_products': top_order_products,
        'top_rating_products': top_rating_products,
        'top_discount_products': top_discount_products,
    })