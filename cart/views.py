from django.shortcuts import render
from .models import CartItem

def cart_view(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    
    return render(request, 'pages/cart.html', context)
