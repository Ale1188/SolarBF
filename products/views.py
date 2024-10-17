from .models import Product, Category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def is_staff_or_worker(user):
    return user.is_staff or user.role == 'worker' 

@login_required
@user_passes_test(is_staff_or_worker)
def management(request):
    return render(request, 'admin/management.html')

@login_required
def product_list(request):
    products = Product.objects.all()
    
    return render(request, 'store/products.html', {
        'products': products,
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('home')
    else:
        form = ProductForm()
    
    return render(request, 'admin/add_product.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})