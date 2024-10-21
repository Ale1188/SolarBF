from django.shortcuts import render, redirect
from .models import Cart, CartItem
from products.models import Product, Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, f'There is not enough stock. Only {product.stock} left available')
        return redirect('products')

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    
    messages.success(request, f'{product.name} add to cart!')
    return redirect('products')

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    cart_items = cart.items.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    coupon_discount = 0
    coupon_code = request.session.get('coupon_code', None)
    
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
                if coupon.discount_type == 'percentage':
                    coupon_discount = cart_total * (coupon.discount_value / 100)
                elif coupon.discount_type == 'fixed_amount':
                    coupon_discount = coupon.discount_value
        except Coupon.DoesNotExist:
            request.session.pop('coupon_code', None)

    if request.method == "POST":
        if 'coupon_code' in request.POST:
            coupon_code = request.POST.get('coupon_code')
            try:
                coupon = Coupon.objects.get(code=coupon_code)

                if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
                    if coupon.discount_type == 'percentage':
                        coupon_discount = cart_total * (coupon.discount_value / 100)
                    elif coupon.discount_type == 'fixed_amount':
                        coupon_discount = coupon.discount_value

                    request.session['coupon_code'] = coupon_code

            except Coupon.DoesNotExist:
                pass

        if 'remove_coupon' in request.POST:
            coupon_discount = 0
            coupon_code = None
            request.session.pop('coupon_code', None)

    final_total = cart_total - coupon_discount

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'final_total': final_total,
        'coupon_discount': coupon_discount,
        'coupon_code': coupon_code,
    })


@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')
