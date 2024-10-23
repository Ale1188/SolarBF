import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Coupon
from orders.models import ShippingAddress, Order, OrderItem 
from django.utils import timezone
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "You don't have items in your cart.")
        return redirect('cart:view_cart')

    user = request.user
    initial_data = {
        'street_address': user.street_address if user.street_address else '',
        'city': user.city if user.city else '',
        'state': user.state if user.state else '',
        'zip_code': user.zip_code if user.zip_code else '',
        'country': user.country if user.country else '',
    }

    cart_items = cart.items.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

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
        recipient_name = request.POST.get('recipient_name')
        street_address = request.POST.get('street_address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        postal_code = request.POST.get('zip_code')
        country = request.POST.get('country')

        if not all([recipient_name, street_address, state, city, postal_code, country]):
            messages.error(request, 'Please complete all address fields.')
            return redirect('checkout')

        shipping_address = ShippingAddress.objects.create(
            user=user,
            address=street_address,
            state = state,
            city=city,
            postal_code=postal_code,
            country = country
        )
        
        order = Order.objects.create(
            user=user,
            order_total=final_total,
            shipping_address=shipping_address,
            is_paid=False
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'mxn',
                        'product_data': {
                            'name': 'Total Order',
                        },
                        'unit_amount': int(final_total * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://127.0.0.1:8000/checkout/success/?order_id={order.id}',
                cancel_url='http://127.0.0.1:8000/cart/',
                billing_address_collection='required',
            )
            return redirect(session.url, code=303)
        except Exception as e:
            messages.error(request, f"An error occurred while creating the payment session: {str(e)}")
            return redirect('checkout')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'coupon_code': coupon_code,
        'coupon_discount': coupon_discount,
        'final_total': final_total,
        'initial_data': initial_data,
    })


@login_required
def success(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return redirect('checkout')

    order = Order.objects.get(id=order_id, user=request.user)
    order.is_paid = True
    order.save()

    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
    except Cart.DoesNotExist:
        pass

    coupon_code = request.session.get('coupon_code', None)
    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code).first()
        if coupon and coupon.uses < coupon.max_uses:
            coupon.uses += 1
            coupon.save()
        del request.session['coupon_code']
    
    shipping_address = order.shipping_address

    return render(request, 'store/success.html', {
        'order': order,
        'street_address': shipping_address.address,
        'city': shipping_address.city,
        'state': shipping_address.state,
        'zip_code': shipping_address.postal_code,
        'country': shipping_address.country,
    })