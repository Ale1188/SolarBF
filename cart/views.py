from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product, Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


def calculate_coupon_discount(coupon, cart_total):
    """Calculate the discount based on the coupon type."""
    if coupon.discount_type == 'percentage':
        return cart_total * (coupon.discount_value / 100)
    return coupon.discount_value


def validate_coupon(coupon_code, cart_total):
    """Validate coupon and return the discount if valid, otherwise return errors."""
    try:
        coupon = Coupon.objects.get(code=coupon_code)
        if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
            return calculate_coupon_discount(coupon, cart_total), True, None
        return 0, False, "The coupon is expired or has reached its usage limit."
    except Coupon.DoesNotExist:
        return 0, False, "The coupon code does not exist."


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(request, f'There is not enough stock. Only {product.stock} left available.')
        return redirect('products')

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    cart_item.quantity = cart_item.quantity + quantity if not created else quantity
    product.stock -= quantity

    cart_item.save()
    product.save()
    cart.last_updated = timezone.now()
    cart.save()

    messages.success(request, f'{product.name} added to cart!')
    return redirect('products')


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if timezone.now() - cart.last_updated > timezone.timedelta(hours=1) and not request.session.get('cart_cleared'):
        for cart_item in cart.items.all():
            cart_item.product.stock += cart_item.quantity
            cart_item.product.save()
        cart.items.all().delete()
        request.session['cart_cleared'] = True
        messages.info(request, "Your cart has been cleared due to inactivity.")
        return redirect('cart')

    if request.session.get('cart_cleared') and cart.items.exists():
        request.session.pop('cart_cleared', None)

    cart_items = cart.items.select_related('product').all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    coupon_discount = 0
    coupon_code = request.session.get('coupon_code')
    valid_coupon = False

    if coupon_code:
        coupon_discount, valid_coupon, error = validate_coupon(coupon_code, cart_total)
        if error:
            messages.error(request, error)
            request.session.pop('coupon_code', None)
            return redirect('cart')

    if request.method == "POST":
        if 'coupon_code' in request.POST:
            coupon_code = request.POST.get('coupon_code')
            coupon_discount, valid_coupon, error = validate_coupon(coupon_code, cart_total)
            if valid_coupon:
                request.session['coupon_code'] = coupon_code
                messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
            else:
                request.session.pop('coupon_code', None)
                messages.error(request, error)
            return redirect('cart')

        if 'remove_coupon' in request.POST:
            request.session.pop('coupon_code', None)
            messages.info(request, "Coupon removed.")
            return redirect('cart')

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
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.product.stock += cart_item.quantity
    cart_item.product.save()
    cart_item.delete()

    messages.info(request, f'Removed {cart_item.product.name} from cart.')
    return redirect('cart')
