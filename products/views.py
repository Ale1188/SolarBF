from .models import Product, Category, Coupon
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm, CategoryForm, CouponForm
from django.contrib import messages
from django.http import JsonResponse
from accounts.views import is_admin, is_staff
import os

@login_required(login_url='login')
def product_view(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})


@login_required
@user_passes_test(is_staff)
def management(request):
    return render(request, 'admin/management.html')


@login_required
@user_passes_test(is_staff)
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin/product_list.html', {'products': products, 'categories': categories})


@login_required
@user_passes_test(is_admin)
def add_product(request):
    return handle_product_form(request, ProductForm(), 'admin/add_product.html', 'Product added successfully!', 'management')


@login_required
@user_passes_test(is_staff)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return handle_product_form(request, ProductForm(instance=product), 'admin/edit_product.html', 'Product updated successfully!', 'product_list', product)


@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.image:
        if os.path.isfile(product.image.path):
            os.remove(product.image.path)
    
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')


@login_required
@user_passes_test(is_staff)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})


@login_required
@user_passes_test(is_admin)
def add_category(request):
    return handle_category_form(request, CategoryForm(), 'admin/add_category.html', 'Category added successfully!', 'categories')


@login_required
@user_passes_test(is_admin)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return handle_category_form(request, CategoryForm(instance=category), 'admin/edit_category.html', 'Category updated successfully!', 'categories', category)


@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories')


@login_required
@user_passes_test(is_staff)
def coupon_list(request):
    coupons = Coupon.objects.all()
    discount_type_choices = Coupon.COUPON_TYPE_CHOICES
    return render(request, 'admin/coupons.html', {'coupons': coupons, 'discount_type_choices': discount_type_choices})


@login_required
@user_passes_test(is_admin)
def create_coupon(request):
    return handle_coupon_form(request, CouponForm(), 'admin/create_coupon.html', 'Coupon created successfully!', 'coupon')


@login_required
@user_passes_test(is_admin)
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    return handle_coupon_form(request, CouponForm(instance=coupon), 'admin/edit_coupon.html', 'Coupon updated successfully!', 'coupon', coupon)


@login_required
@user_passes_test(is_admin)
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.delete()
    messages.success(request, 'Coupon deleted successfully!')
    return redirect('coupon')


@login_required
@user_passes_test(is_staff)
def coupon_detail(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
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


# Helper functions
def handle_product_form(request, form, template, success_message, redirect_url, product=None):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            if product:
                if product.image and form.cleaned_data['image'] != product.image:
                    if os.path.isfile(product.image.path):
                        os.remove(product.image.path)

            form.save()
            messages.success(request, success_message)
            return redirect(redirect_url)

    return render(request, template, {'form': form, 'product': product})


def handle_category_form(request, form, template, success_message, redirect_url, category=None):
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(redirect_url)
    return render(request, template, {'form': form, 'category': category})


def handle_coupon_form(request, form, template, success_message, redirect_url, coupon=None):
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, success_message)
            return redirect(redirect_url)
    return render(request, template, {'form': form, 'coupon': coupon})
