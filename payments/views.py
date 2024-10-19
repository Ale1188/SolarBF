# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import *
# from cart.models import Cart
# from products.models import Coupon
# from decimal import Decimal
# from django.db import transaction


#@login_required
# def checkout(request):
#     try:
#         cart = Cart.objects.get(user=request.user)
#     except Cart.DoesNotExist:
#         return redirect('cart')  # Redirect if there is no cart

#     cart_items = cart.items.all()
#     cart_total = sum(item.product.price * item.quantity for item in cart_items)
#     coupon_discount = 0
#     coupon_code = request.session.get('coupon_code', None)  # Retrieve the coupon code from the session

#     # Check if a coupon is applied
#     if coupon_code:
#         try:
#             coupon = Coupon.objects.select_for_update().get(code=coupon_code)  # Lock the coupon for update

#             if coupon.valid_from <= timezone.now() <= coupon.valid_to and coupon.uses < coupon.max_uses:
#                 if coupon.discount_type == 'percentage':
#                     coupon_discount = cart_total * (coupon.discount_value / 100)
#                 elif coupon.discount_type == 'fixed_amount':
#                     coupon_discount = coupon.discount_value

#                 # Spend the coupon usage here
#                 coupon.uses += 1
#                 coupon.save()  # Save the updated coupon

#         except Coupon.DoesNotExist:
#             pass

#     final_total = cart_total - coupon_discount

#     if request.method == "POST":
#         # Here you can handle the payment logic and create the order, etc.
#         # ...

#         # After completing the payment, you can clear the coupon code
#         del request.session['coupon_code']

#         return redirect('order_confirmation')  # Redirect to the order confirmation page

#     return render(request, 'store/checkout.html', {
#         'cart_items': cart_items,
#         'cart_total': cart_total,
#         'final_total': final_total,
#         'coupon_discount': coupon_discount,
#         'coupon_code': coupon_code,
#     })