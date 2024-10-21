from django.shortcuts import render, redirect
from cart.models import Cart
from .models import Payment, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Coupon
from django.utils import timezone
from decimal import Decimal

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "You don't have items in your cart.")
        return redirect('cart:view_cart')

    cart_items = cart.items.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    user = request.user
    initial_data = {
        'street_address': user.street_address,
        'city': user.city,
        'state': user.state,
        'zip_code': user.zip_code,
        'country': user.country,
    }
    
    coupon_code = request.session.get('coupon_code', None)
    coupon_discount = Decimal('0.00')

    coupon = None
    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code).first()
        if coupon and coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
            if coupon.discount_type == 'percentage':
                coupon_discount = (cart_total * coupon.discount_value) / 100
            elif coupon.discount_type == 'fixed_amount':
                coupon_discount = coupon.discount_value

            coupon_discount = min(coupon_discount, cart_total)

    final_total = cart_total - coupon_discount

    if request.method == 'POST':
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')

        if not all([street_address, city, state, zip_code, country]):
            messages.error(request, 'Please complete all address fields.')
            return redirect('checkout')

        payment_method = request.POST.get('payment_method')

        if payment_method not in ['credit_card', 'paypal', 'debit']:
            messages.error(request, 'Invalid payment method.')
            return redirect('checkout')

        try:
            order = Order.objects.create(
                user=request.user,
                total_amount=cart_total,
                discount=coupon_discount,
                final_amount=final_total,
                coupon=coupon,
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country
            )
            order.cart_items.set(cart_items)

            payment = Payment.objects.create(
                order=order,
                amount=final_total,
                payment_method=payment_method,
            )

            payment.status = 'completed'
            payment.save()

            order.mark_as_paid()

            cart.items.clear()

            messages.success(request, "Payment successful!")
            return redirect('products')

        except Exception as e:
            messages.error(request, f"An error occurred while processing the payment: {str(e)}")
            return redirect('checkout')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'coupon_code': coupon_code,
        'coupon_discount': coupon_discount,
        'final_total': final_total,
        'initial_data': initial_data,
    })
