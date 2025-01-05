from django.shortcuts import render
from product.models import Brand

def brands_context(request):
    """
    Add brands to the context of all templates.
    """
    brands = Brand.objects.all()
    return {'brands': brands}