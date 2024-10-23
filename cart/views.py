from django.shortcuts import render, redirect
from .models import Cart, CartItem
from products.models import Product, Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(request, f'There is not enough stock. Only {product.stock} left available')
        return redirect('products')

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if item_created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    product.stock -= quantity
    cart_item.save()
    product.save()

    cart.last_updated = timezone.now()
    cart.save()

    return redirect('products')


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Clear cart if inactive for over an hour
    if timezone.now() - cart.last_updated > timezone.timedelta(hours=1):
        clear_cart(cart)
        messages.info(request, "Your cart has been cleared due to inactivity.")
        return redirect('cart')

    cart.last_updated = timezone.now()
    cart.save()

    cart_items = cart.items.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    coupon_discount, valid_coupon, coupon_code = handle_coupons(request, cart_total)

    if request.method == "POST":
        handle_coupon_post(request, cart_total)

    final_total = cart_total - coupon_discount

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'final_total': final_total,
        'coupon_discount': coupon_discount,
        'coupon_code': coupon_code,
        'valid_coupon': valid_coupon,
    })


@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    product = cart_item.product
    product.stock += cart_item.quantity
    product.save()
    cart_item.delete()
    return redirect('cart')


def clear_cart(cart):
    """Clear the cart and return stock to products."""
    for cart_item in cart.items.all():
        product = cart_item.product
        product.stock += cart_item.quantity
        product.save()
    cart.items.all().delete()


def handle_coupons(request, cart_total):
    """Handle coupon validation and discount calculation."""
    coupon_discount = 0
    valid_coupon = False
    coupon_code = request.session.get('coupon_code')

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
                valid_coupon = True
                coupon_discount = (
                    cart_total * (coupon.discount_value / 100)
                    if coupon.discount_type == 'percentage'
                    else coupon.discount_value
                )
            else:
                messages.error(request, "The coupon has expired or reached its usage limit.")
                request.session.pop('coupon_code', None)
        except Coupon.DoesNotExist:
            messages.error(request, "The coupon code does not exist.")
            request.session.pop('coupon_code', None)

    return coupon_discount, valid_coupon, coupon_code


def handle_coupon_post(request, cart_total):
    """Handle coupon submission or removal from the cart."""
    if 'coupon_code' in request.POST:
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
                request.session['coupon_code'] = coupon_code
                messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
            else:
                messages.error(request, "The coupon is expired or reached its usage limit.")
                request.session.pop('coupon_code', None)
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")
            request.session.pop('coupon_code', None)

    if 'remove_coupon' in request.POST:
        request.session.pop('coupon_code', None)
        messages.info(request, "Coupon removed.")
