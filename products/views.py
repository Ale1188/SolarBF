from .models import Product, Category
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@login_required
def productView(request):
    products = Product.objects.all()
    
    return render(request, 'store/products.html', {
        'products': products,
    })



def is_staff_or_worker(user):
    return user.is_staff or user.role == 'worker' 

@login_required
@user_passes_test(is_staff_or_worker)
def management(request):
    return render(request, 'admin/management.html')


# Product
@login_required
@user_passes_test(is_staff_or_worker)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {
        'products': products,
    })

@login_required
@user_passes_test(is_staff_or_worker)
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

@login_required
@user_passes_test(is_staff_or_worker)
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')


# Category
@login_required
@user_passes_test(is_staff_or_worker)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_staff_or_worker)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category.html', {'form': form})

@login_required
@user_passes_test(is_staff_or_worker)
def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/edit_category.html', {'form': form, 'category': category})

@login_required
@user_passes_test(is_staff_or_worker)
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('category_list')