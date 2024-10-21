from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from accounts.views import is_admin, is_staff
from django.http import JsonResponse

@login_required
def productView(request):
    products = Product.objects.all()
    
    return render(request, 'store/products.html', {
        'products': products,
    })

@login_required
@user_passes_test(is_staff)
def management(request):
    return render(request, 'admin/management.html')


# Product
@login_required
@user_passes_test(is_staff)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {
        'products': products,
    })

@login_required
@user_passes_test(is_admin)
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
@user_passes_test(is_staff)
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

@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')


# Category
@login_required
@user_passes_test(is_staff)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('category_list')


# Coupon
@login_required
@user_passes_test(is_staff)
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'admin/coupons.html', {'coupons': coupons})

@login_required
@user_passes_test(is_admin)
def create_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupon')
    else:
        form = CouponForm()
    return render(request, 'admin/create_coupon.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    messages.success(request, 'Coupon deleted successfully!')
    return redirect('coupon')

# @login_required
# @user_passes_test(is_admin)
# def edit_coupon(request, coupon_id):
#     coupon = Coupon.objects.get(id=coupon_id)
#     coupon.delete()
#     messages.success(request, 'Coupon edit successfully!')
#     return redirect('coupon')

@login_required
@user_passes_test(is_admin)
def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon updated successfully!')
            return redirect('coupon')
    else:
        form = CouponForm(instance=coupon)
    
    return render(request, 'admin/edit_coupon.html', {'form': form, 'coupon': coupon})

@login_required
@user_passes_test(is_staff)
def coupon_detail(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon_data = {
        'code': coupon.code,
        'discount_value': coupon.discount_value,
        'discount_type': coupon.discount_type,
        'valid_from': coupon.valid_from,
        'valid_to': coupon.valid_to,
        'uses': coupon.uses,
        'max_uses': coupon.max_uses,
    }
    return JsonResponse(coupon_data)