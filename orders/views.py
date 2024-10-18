from .models import Product, Category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def productView(request):
    products = Product.objects.all()
    
    return render(request, 'store/products.html', {
        'products': products,
    })
